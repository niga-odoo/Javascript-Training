// console.log("It's working!!!")
display = () => {
    // console.log("It's working from display!!!")

    //Redirect Page
    window.location.href = '/products';
}

// dispatchEvent
// let btn = document.querySelector('.btn');

// btn.addEventListener('clicks', function () {
//     window.alert('Mouse Clicked');
// });

// let clickEvent = new Event('clicks');
// btn.dispatchEvent(clickEvent);

// Waiting for Intervals
setInterval(myFunction, 1000);

function myFunction() {
  let d = new Date();
  return d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds();
}