import qrcode from 'qrcode';

const userDetail = () => {
  const img = document.querySelector('#qr_img')
  if (img) {
    const token = img.getAttribute('name')
    console.log(token)
    const opts = {
      errorCorrectionLevel: 'H',
      type: 'image/png',
      rendererOpts: {
        quality: 0.5
      }
    }
    qrcode.toDataURL(token, opts)
      .then(data => img.setAttribute('src', data))    
  }
}

export default userDetail
