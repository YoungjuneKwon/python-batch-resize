def validate_path(p):
    import os, re
    ps = p.split(os.path.sep)
    ps = ps[:-1] if re.match('.*\..{1,4}', ps[-1]) else ps
    [os.mkdir(os.path.sep.join(ps[:i])) for i in range(2, len(ps) + 1)  if not os.path.exists(os.path.sep.join(ps[:i]))]
    return p

def rotate_with(img, r_dict):
    from PIL import ExifTags
    r = img.info['parsed_exif'][{v:k for k, v in ExifTags.TAGS.items()}['Orientation']]
    if not r in r_dict: return img
    i2 = img.rotate(r_dict[r], expand=True)
    i2.info['exif'] = img.info['exif']
    i2.info['parsed_exif'] = img.info['parsed_exif']
    return i2
    
def adjust_rotation(img):
    return rotate_with(img, {3: 180, 6: 270, 8: 90})

def restore_rotation(img):
    return rotate_with(img, {3: 180, 6: 90, 8: 270})

def resize_and_crop(org, dst, size, center=(0.5, 0.5)):
    from PIL import Image, JpegImagePlugin as JIP
    img = adjust_rotation(Image.open(org))
    org_r = img.size[1] / img.size[0]
    dst_r = size[1] / size[0]

    s1 = (size[0], int(size[0] * org_r)) if org_r > dst_r else (int(size[1] / org_r), size[1])
    d = [int((s1[i] - size[i]) / 2) for i in (0, 1)]
    c = [int((0.5 - center[i]) * s1[i]) for i in (0, 1)]
    i2 = img.resize(s1).crop((d[0] - c[0], d[1] - c[1], s1[0] - d[0] - c[0], s1[1] - d[1] - c[1]))
    restore_rotation(i2.resize(size)).save(validate_path(dst), 'JPEG', optimize=True, exif=img.info['exif'], icc_profile = img.info.get('icc_profile',''), subsampling=JIP.get_sampling(img))
    return i2
