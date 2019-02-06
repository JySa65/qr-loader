import swal from 'sweetalert2'
import axios from 'axios'
import mobile from '../../utils/mobile'

const qr = () => {
  const video = document.getElementById('preview')
  if (video) {
    const scanner = new Instascan.Scanner({ video });
    const type = mobile.any()
    Instascan.Camera.getCameras().then((cameras) => {
      if (cameras.length > 0) {
        if (type === null) {
          scanner.start(cameras[0]);
        } else {
          scanner.start(cameras[1]);
        }
        const preload = document.querySelector('#preload')
        const video = document.querySelector('#video')
        video.removeAttribute('hidden')
        preload.setAttribute('hidden', 'hidden')
      } else {
        swal.fire('Error', 'Camera No Found', 'error')
      }
    }).catch((e) => {
      swal.fire('Error', e, 'error')
    });

    scanner.addListener('scan', async (content) => {
      const data = await axios.get(`scan-qr/?token=${content}`)
      if (data.data.status) {
        if (!data.data.data.type) {
          swal.fire({
            type: 'warning',
            titleText: data.data.msg,
            text: '¿Desea Registrarlo A Un Persona?',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si',
            cancelButtonText: 'No'
          })
            .then((result) => {
              if (result.value) {
                window.location.href = `/user/create/${data.data.data.token}/`
              }
            })
        } else {
          swal.fire({
            type: 'success',
            titleText: data.data.msg,
            text: '¿Desea Verlo?',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Si',
            cancelButtonText: 'No'
          })
            .then((result) => {
              if (result.value) {
                window.location.href = `/user/detail/${data.data.data.token}/`
              }
            })
        }
      } else {
        swal.fire('Error', data.data.msg, 'error')
      }
    });
  }
}

export default qr
