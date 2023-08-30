#机器学习板块：
def get_res(img_path):
    #from paddleocr import PaddleOCR, draw_ocr
    from paddleocr import PaddleOCR,draw_ocr
    import os
    # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
    # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    # 显示结果
    # 如果本地没有simfang.ttf，可以在doc/fonts目录下下载
    from PIL import Image
    result = result[0]
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    im_show = draw_ocr(image, boxes, txts, scores, font_path='doc/fonts/simfang.ttf')
    im_show = Image.fromarray(im_show)

    path = './static/ocrRes'
    files = os.listdir(path)
    #获取服务器已经存储的图片数量
    i = len(files)
    # 从配置文件中载入图片保存路径
    resImg_path = f'./static/ocrRes/{i+1}.png'
    im_show.save(resImg_path)
    resImg_path=resImg_path[9:]
    return txts,scores,resImg_path

#'./static/uploads/{i+1}.png'
def print_res(img_path):  #img_path为待识别图片完整的绝对路径
    img_path1=f'D:/2023实训/OCRplatform'+img_path[1:]
    print('path1',img_path1)
    res,scores,resPath=get_res(img_path1)
    return res,scores,resPath

#接口说明：

#需要其他后端同学把上传的图片存到本地，并且把图片的绝对路径传给这个接口，就可以输出识别的结果了
#可以修改get_res返回的结果来决定最终输出哪些数据，
#当只返回txts文本时，输出的数据包括：识别到的所有字符组成的数组：
#eg.
#['热卖', '前1小时', '前1小时', '减20元', '减20元', '明星组合', '限时好礼', '前1小时', '899元', '全场低至', '减20元', '79.9元', '立即抢购>', '送', '买送', '抗初老', '限量版', '明星套组', '限量明星组#合', '进口', '限时好礼', '899元', '商品', '拍下', '2瓶装', '减20', '拍下', 'TOP1', '12期', '50', '法国进口', '免息', '元', '知乎@小张Python']
#目前的接口设置成了返回txts文本和准确率scores（eg. 0.8392305374145508，16位小数组成的数组)
#后端的同学可以对其进行处理

#关于正则表达式：
#前端将正则表达式字符串和图片传给后端，后端同学将图片的绝对路径传给这个接口，接口返回的数据格式同上，后端同学对txts文本数组进行正则表达式匹配，返回结果给前端。



