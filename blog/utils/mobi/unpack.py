"""
    this code from kindleUnpack
"""
import os

from blog.utils.mobi.compatibility_utils import unicode_str
from blog.utils.mobi.unpack_structure import FileNames
from blog.utils.mobi.mobi_sectioner import Sectionizer
from blog.utils.mobi.mobi_header import MobiHeader
from blog.utils.mobi.mobi_cover import CoverProcessor
from blog.utils.mobi.split import mobi_split
from blog.utils.mobi.unipath import pathof


DUMP = False
""" Set to True to dump all possible information. """

WRITE_RAW_DATA = False
""" Set to True to create additional files with raw data for debugging/reverse engineering. """

SPLIT_COMBO_MOBIS = False
""" Set to True to split combination mobis into mobi7 and mobi8 pieces. """

CREATE_COVER_PAGE = True  # XXX experimental
""" Create and insert a cover xhtml page. """

EOF_RECORD = b'\xe9\x8e' + b'\r\n'
""" The EOF record content. """

TERMINATION_INDICATOR1 = b'\x00'
TERMINATION_INDICATOR2 = b'\x00\x00'
TERMINATION_INDICATOR3 = b'\x00\x00\x00'

KINDLEGENSRC_FILENAME = "kindlegensrc.zip"
""" The name for the kindlegen source archive. """

KINDLEGENLOG_FILENAME = "kindlegenbuild.log"
""" The name for the kindlegen build log. """

K8_BOUNDARY = b'BOUNDARY'

text_type = str
binary_type = bytes

class unpackException(Exception):
    pass


def unpack_book(model,
                outdir,
                apnxfile=None,
                epubver='2',
                use_hd=False,
                dodump=False,
                dowriteraw=False,
                dosplitcombos=False):
    global DUMP
    global WRITE_RAW_DATA
    global SPLIT_COMBO_MOBIS
    infile = model.file
    if DUMP or dodump:
        DUMP = True
    if WRITE_RAW_DATA or dowriteraw:
        WRITE_RAW_DATA = True
    if SPLIT_COMBO_MOBIS or dosplitcombos:
        SPLIT_COMBO_MOBIS = True

    infile = unicode_str(infile)
    outdir = unicode_str(outdir)
    if apnxfile is not None:
        apnxfile = unicode_str(apnxfile)

    files = FileNames(infile, outdir)
    # process the PalmDoc database header and verify it is a mobi
    sect = Sectionizer(infile)
    if sect.ident != b'BOOKMOBI' and sect.ident != b'TEXtREAd':
        raise unpackException('Invalid file format')
    if DUMP:
        sect.dumppalmheader()
    else:
        print("Palm DB type: %s, %d sections." % (sect.ident.decode('utf-8'),sect.num_sections))

    mhlst = []
    mh = MobiHeader(sect, 0)
    # if this is a mobi8-only file hasK8 here will be true
    mhlst.append(mh)
    K8Boundary = -1

    if mh.isK8():
        print('Unpacking a KF8 book...')
        hasK8 = True
    else:
        # This is either a Mobipocket 7 or earlier, or a combi M7/KF8
        # Find out which
        hasK8 = False
        for i in range(len(sect.sectionoffsets)-1):
            before, after = sect.sectionoffsets[i:i+2]
            if (after - before) == 8:
                data = sect.loadSection(i)
                if data == K8_BOUNDARY:
                    sect.setsectiondescription(i,"Mobi/KF8 Boundary Section")
                    mh = MobiHeader(sect,i+1)
                    hasK8 = True
                    mhlst.append(mh)
                    K8Boundary = i
                    break
        if hasK8:
            print("Unpacking a Combination M{0:d}/KF8 book...".format(mh.version))
            if SPLIT_COMBO_MOBIS:
                # if this is a combination mobi7-mobi8 file split them up
                mobisplit = mobi_split(infile)
                if mobisplit.combo:
                    outmobi7 = os.path.join(
                        files.outdir,
                        'mobi7-' + files.getInputFileBasename() + '.mobi')
                    outmobi8 = os.path.join(
                        files.outdir,
                        'mobi8-' + files.getInputFileBasename() + '.azw3')
                    with open(pathof(outmobi7), 'wb') as f:
                        f.write(mobisplit.getResult7())
                    with open(pathof(outmobi8), 'wb') as f:
                        f.write(mobisplit.getResult8())
        else:
            print("Unpacking a Mobipocket {0:d} book...".format(mh.version))

    if hasK8:
        files.makeK8Struct()

    # process all mobi headers
    rscnames = []
    rsc_ptr = -1
    k8resc = None
    obfuscate_data = []
    for mh in mhlst:
        pagemapproc = None
        if mh.isK8():
            sect.setsectiondescription(mh.start,"KF8 Header")
            mhname = os.path.join(files.outdir,"header_K8.dat")
            print("Processing K8 section of book...")
        elif mh.isPrintReplica():
            sect.setsectiondescription(mh.start,"Print Replica Header")
            mhname = os.path.join(files.outdir,"header_PR.dat")
            print("Processing PrintReplica section of book...")
        else:
            if mh.version == 0:
                sect.setsectiondescription(mh.start,
                                           "PalmDoc Header".format(mh.version))
            else:
                sect.setsectiondescription(
                    mh.start, "Mobipocket {0:d} Header".format(mh.version))
            mhname = os.path.join(files.outdir, "header.dat")
            print("Processing Mobipocket {0:d} section of book...".format(
                mh.version))

        if DUMP:
            # write out raw mobi header data
            with open(pathof(mhname), 'wb') as f:
                f.write(mh.header)

    metadata = mh.get_meta_data()
    mh.describe_header(DUMP)
    if mh.is_encrypted():
        raise unpackException('Book is encrypted')

    print("Unpacking images, resources, fonts, etc")
    beg = mh.firstresource
    end = sect.num_sections
    if beg < K8Boundary:
        # processing first part of a combination file
        end = K8Boundary
    cover_offset = int(metadata.get('CoverOffset', ['-1'])[0])
    if not CREATE_COVER_PAGE:
        cover_offset = None
    
    for i in range(beg, end):
        data = sect.loadSection(i)
        type = data[0:4]

        # handle the basics first
        if type in [b"FLIS", b"FCIS", b"FDST", b"DATP"]:
            if DUMP:
                fname = unicode_str(type) + "%05d" % i
                if mh.isK8():
                    fname += "_K8"
                fname += '.dat'
                outname= os.path.join(files.outdir, fname)
                with open(pathof(outname), 'wb') as f:
                    f.write(data)
                print("Dumping section {0:d} type {1:s} to file {2:s} ".format(i,unicode_str(type),outname))
            sect.setsectiondescription(i,"Type {0:s}".format(unicode_str(type)))
            rscnames.append(None)
        elif type == b"SRCS":
            rscnames = processSRCS(i, files, rscnames, sect, data)
        elif type == b"PAGE":
            rscnames, pagemapproc = processPAGE(i, files, rscnames, sect, data, mh, pagemapproc)
        elif type == b"CMET":
            rscnames = processCMET(i, files, rscnames, sect, data)
        elif type == b"FONT":
            rscnames, obfuscate_data, rsc_ptr = processFONT(i, files, rscnames, sect, data, obfuscate_data, beg, rsc_ptr)
        elif type == b"CRES":
            rscnames, rsc_ptr = processCRES(i, files, rscnames, sect, data, beg, rsc_ptr, use_hd)
        elif type == b"CONT":
            rscnames = processCONT(i, files, rscnames, sect, data)
        elif type == b"kind":
            rscnames = processkind(i, files, rscnames, sect, data)
        elif type == b'\xa0\xa0\xa0\xa0':
            sect.setsectiondescription(i,"Empty_HD_Image/Resource_Placeholder")
            rscnames.append(None)
            rsc_ptr += 1
        elif type == b"RESC":
            rscnames, k8resc = processRESC(i, files, rscnames, sect, data, k8resc)
        elif data == EOF_RECORD:
            sect.setsectiondescription(i,"End Of File")
            rscnames.append(None)
        elif data[0:8] == b"BOUNDARY":
            sect.setsectiondescription(i,"BOUNDARY Marker")
            rscnames.append(None)
        else:
            # if reached here should be an image ow treat as unknown
            rscnames, rsc_ptr  = processImage(i, files, rscnames, sect, data, beg, rsc_ptr, cover_offset)
    # done unpacking resources


def processSRCS(i, files, rscnames, sect, data):
    # extract the source zip archive and save it.
    print("File contains kindlegen source archive, extracting as %s" % KINDLEGENSRC_FILENAME)
    srcname = os.path.join(files.outdir, KINDLEGENSRC_FILENAME)
    with open(pathof(srcname), 'wb') as f:
        f.write(data[16:])
    rscnames.append(None)
    sect.setsectiondescription(i,"Zipped Source Files")
    return rscnames

def processPAGE(i, files, rscnames, sect, data, mh, pagemapproc):
    # process any page map information and create an apnx file
    pagemapproc = PageMapProcessor(mh, data)
    rscnames.append(None)
    sect.setsectiondescription(i,"PageMap")
    apnx_meta = {}
    acr = sect.palmname.decode('latin-1').rstrip('\x00')
    apnx_meta['acr'] = acr
    apnx_meta['cdeType'] = mh.metadata['cdeType'][0]
    apnx_meta['contentGuid'] = hex(int(mh.metadata['UniqueID'][0]))[2:]
    apnx_meta['asin'] = mh.metadata['ASIN'][0]
    apnx_meta['pageMap'] = pagemapproc.getPageMap()
    if mh.version == 8:
        apnx_meta['format'] = 'MOBI_8'
    else:
        apnx_meta['format'] = 'MOBI_7'
    apnx_data = pagemapproc.generateAPNX(apnx_meta)
    if mh.isK8():
        outname = os.path.join(files.outdir, 'mobi8-'+files.getInputFileBasename() + '.apnx')
    else:
        outname = os.path.join(files.outdir, 'mobi7-'+files.getInputFileBasename() + '.apnx')
    with open(pathof(outname), 'wb') as f:
        f.write(apnx_data)
    return rscnames, pagemapproc

def processCMET(i, files, rscnames, sect, data):
    # extract the build log
    print("File contains kindlegen build log, extracting as %s" % KINDLEGENLOG_FILENAME)
    srcname = os.path.join(files.outdir, KINDLEGENLOG_FILENAME)
    with open(pathof(srcname), 'wb') as f:
        f.write(data[10:])
    rscnames.append(None)
    sect.setsectiondescription(i,"Kindlegen log")
    return rscnames

def processFONT(i, files, rscnames, sect, data, obfuscate_data, beg, rsc_ptr):
    fontname = "font%05d" % i
    ext = '.dat'
    font_error = False
    font_data = data
    try:
        usize, fflags, dstart, xor_len, xor_start = struct.unpack_from(b'>LLLLL',data,4)
    except:
        print("Failed to extract font: {0:s} from section {1:d}".format(fontname,i))
        font_error = True
        ext = '.failed'
        pass
    if not font_error:
        print("Extracting font:", fontname)
        font_data = data[dstart:]
        extent = len(font_data)
        extent = min(extent, 1040)
        if fflags & 0x0002:
            # obfuscated so need to de-obfuscate the first 1040 bytes
            key = bytearray(data[xor_start: xor_start+ xor_len])
            buf = bytearray(font_data)
            for n in range(extent):
                buf[n] ^=  key[n%xor_len]
            font_data = bytes(buf)
        if fflags & 0x0001:
            # ZLIB compressed data
            font_data = zlib.decompress(font_data)
        hdr = font_data[0:4]
        if hdr == b'\0\1\0\0' or hdr == b'true' or hdr == b'ttcf':
            ext = '.ttf'
        elif hdr == b'OTTO':
            ext = '.otf'
        else:
            print("Warning: unknown font header %s" % hexlify(hdr))
        if (ext == '.ttf' or ext == '.otf') and (fflags & 0x0002):
            obfuscate_data.append(fontname + ext)
        fontname += ext
        outfnt = os.path.join(files.imgdir, fontname)
        with open(pathof(outfnt), 'wb') as f:
            f.write(font_data)
        rscnames.append(fontname)
        sect.setsectiondescription(i,"Font {0:s}".format(fontname))
        if rsc_ptr == -1:
            rsc_ptr = i - beg
    return rscnames, obfuscate_data, rsc_ptr

def processCRES(i, files, rscnames, sect, data, beg, rsc_ptr, use_hd):
    # extract an HDImage
    global DUMP
    data = data[12:]
    imgtype = get_image_type(None, data)

    if imgtype is None:
        print("Warning: CRES Section %s does not contain a recognised resource" % i)
        rscnames.append(None)
        sect.setsectiondescription(i,"Mysterious CRES data, first four bytes %s" % describe(data[0:4]))
        if DUMP:
            fname = "unknown%05d.dat" % i
            outname= os.path.join(files.outdir, fname)
            with open(pathof(outname), 'wb') as f:
                f.write(data)
            sect.setsectiondescription(i,"Mysterious CRES data, first four bytes %s extracting as %s" % (describe(data[0:4]), fname))
        rsc_ptr += 1
        return rscnames, rsc_ptr

    if use_hd:
        # overwrite corresponding lower res image with hd version
        imgname = rscnames[rsc_ptr]
        imgdest = files.imgdir
    else:
        imgname = "HDimage%05d.%s" % (i, imgtype)
        imgdest = files.hdimgdir
    print("Extracting HD image: {0:s} from section {1:d}".format(imgname,i))
    outimg = os.path.join(imgdest, imgname)
    with open(pathof(outimg), 'wb') as f:
        f.write(data)
    rscnames.append(None)
    sect.setsectiondescription(i,"Optional HD Image {0:s}".format(imgname))
    rsc_ptr += 1
    return rscnames, rsc_ptr

def processCONT(i, files, rscnames, sect, data):
    global DUMP
    # process a container header, most of this is unknown
    # right now only extract its EXTH
    dt = data[0:12]
    if dt == b"CONTBOUNDARY":
        rscnames.append(None)
        sect.setsectiondescription(i,"CONTAINER BOUNDARY")
    else:
        sect.setsectiondescription(i,"CONT Header")
        rscnames.append(None)
        if DUMP:
            cpage, = struct.unpack_from(b'>L', data, 12)
            contexth = data[48:]
            print("\n\nContainer EXTH Dump")
            dump_contexth(cpage, contexth)
            fname = "CONT_Header%05d.dat" % i
            outname= os.path.join(files.outdir, fname)
            with open(pathof(outname), 'wb') as f:
                f.write(data)
    return rscnames

def processkind(i, files, rscnames, sect, data):
    global DUMP
    dt = data[0:12]
    if dt == b"kindle:embed":
        if DUMP:
            print("\n\nHD Image Container Description String")
            print(data)
        sect.setsectiondescription(i,"HD Image Container Description String")
        rscnames.append(None)
    return rscnames

def processRESC(i, files, rscnames, sect, data, k8resc):
    global DUMP
    if DUMP:
        rescname = "RESC%05d.dat" % i
        print("Extracting Resource: ", rescname)
        outrsc = os.path.join(files.outdir, rescname)
        with open(pathof(outrsc), 'wb') as f:
            f.write(data)
    if True:  # try:
        # parse the spine and metadata from RESC
        k8resc = K8RESCProcessor(data[16:], DUMP)
    else:  # except:
        print("Warning: cannot extract information from RESC.")
        k8resc = None
    rscnames.append(None)
    sect.setsectiondescription(i,"K8 RESC section")
    return rscnames, k8resc

def processImage(i, files, rscnames, sect, data, beg, rsc_ptr, cover_offset):
    global DUMP
    # Extract an Image
    imgtype = get_image_type(None, data)
    if imgtype is None:
        print("Warning: Section %s does not contain a recognised resource" % i)
        rscnames.append(None)
        sect.setsectiondescription(i,"Mysterious Section, first four bytes %s" % describe(data[0:4]))
        if DUMP:
            fname = "unknown%05d.dat" % i
            outname= os.path.join(files.outdir, fname)
            with open(pathof(outname), 'wb') as f:
                f.write(data)
            sect.setsectiondescription(i,"Mysterious Section, first four bytes %s extracting as %s" % (describe(data[0:4]), fname))
        return rscnames, rsc_ptr

    imgname = "image%05d.%s" % (i, imgtype)
    if cover_offset is not None and i == beg + cover_offset:
        imgname = "cover%05d.%s" % (i, imgtype)
    print("Extracting image: {0:s} from section {1:d}".format(imgname,i))
    outimg = os.path.join(files.imgdir, imgname)
    with open(pathof(outimg), 'wb') as f:
        f.write(data)
    rscnames.append(imgname)
    sect.setsectiondescription(i,"Image {0:s}".format(imgname))
    if rsc_ptr == -1:
        rsc_ptr = i - beg
    return rscnames, rsc_ptr