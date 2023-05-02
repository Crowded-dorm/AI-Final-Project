from interact import selectSourceImage
from ai import findNearDuplicateImages

def getImgList(folder_path: str):
    raise "Not implemented!"

if __name__ == '__main__':
    folder_path = 'assets'
    img_arr = getImgList(folder_path)
    img = selectSourceImage(img_arr)
    choices = findNearDuplicateImages(img)
    #
