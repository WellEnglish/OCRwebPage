<template>
  <div class="above">
    <el-row :gutter="20">
      <el-col :span="13">
        <div class="grid-content bg-purple">
          <el-card :body-style="{ padding: '6px' }"  shadow="hover">
            <img src="@/assets/pic/ocr_index.png" class="img">
          <div style="padding: 14px;">
            <span style="font-family: Manyu;font-size:6vh;float:left;">OCR OFFLINE</span>
            <div class="bottom clearfix">
              <time class="time" style="font-family: FMwr;font-size:3vh;float: right;">{{ currentDate }}</time>
              <el-button type="text" class="button" style="margin-right: 2vh;float: right;font-size: 3vh;font-family: Jiyi;">
                关于
              </el-button>
            </div>
          </div>
          </el-card>
        </div>
      </el-col>
      <el-col :span="11">
        <div class="grid-content bg-purple-light">
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span style="font-family: Manyu;font-size:5vh;">OCR OFFLINE</span>
              <el-button type="text" class="button" style="margin-right: 2vh;float: right;font-size: 3vh;font-family: Jiyi;">
                关于
              </el-button>
            </div>
            <div class="text" style="margin-top:2vh">
              <span style="font-family: Jiyi;font-size:3vh;">
              OCR（Optical Character Recognition）光学字符识别技术是一种可以将图像中的文本转换为可编辑、可搜索的文本的技术。OCR离线服务是指可以在没有网络连接的情况下使用OCR技术进行文本识别服务。
              </span>
              <br>
            </div>
            <div class="text" style="margin-top:3vh">
              <span style="font-family: Jiyi;font-size:3vh;">
                相对于在线OCR服务，离线OCR服务具有更快的识别速度、更好的隐私保护、更稳定的服务，因此在需要大量文本识别的场景中可以提供更高效的解决方案。在一些特殊环境下，如接入网络有限、隐私数据无法外传等情况，离线OCR服务可以克服在线OCR服务的不足，更好地满足用户的需求。
              </span>
            </div>
            <div class="text" style="margin-top:3vh">
              <span style="font-family: Jiyi;font-size:3vh;">
              基于OCR离线服务的技术优势，越来越多的应用场景可以采用OCR离线服务，如文档OCR识别、照片相册自动识别、证件身份证识别、车牌号码识别等。
              </span>
            </div>
          </el-card>
        </div>
      </el-col>
</el-row>
  </div>
</template>
<script>
  export default{
    data(){
      return {
        currentDate:new Date()
      };
    }
  }
</script>

<style>
  .bg-purple{
    margin-left: 3vh;
    margin-top: 3vh;
  }
  .bg-purple-light{
    margin-top: 3vh;
    margin-right: 1vh;
  }
  .img{
    width:85vh;
    height: 50vh;
  }
</style>