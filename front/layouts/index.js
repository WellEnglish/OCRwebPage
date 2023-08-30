module.exports = {
  webpackBarName: 'vue-admin-better',
  webpackBanner:
    ' build: vue-admin-better \n vue-admin-beautiful.com \n https://gitee.com/chu1204505056/vue-admin-better \n time: ',
  donationConsole() {
    const chalk = require('chalk')
    console.log(
      chalk.green(
        `> 欢迎使用OCR OFFLINE`
      )
    )
    
    console.log(chalk.green(`> 如果您不希望显示以上信息，可在config中配置关闭`))
    console.log('\n')
  },
}
