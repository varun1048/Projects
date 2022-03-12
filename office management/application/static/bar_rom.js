const countdown = () => {
    let timer = document.getElementById("timer");
    let dt = new Date();
    let h = dt.getHours();
    let m = dt.getMinutes();
    let s = dt.getSeconds();

    // minutes remaining until next 10 minute mark
    m = s ? 9 - (m % 10) : 10 - (m % 10);

    // seconds remaining until next minute mark
    if (s) {
      s = 60 - s;
    }

    timer.textContent = `${m}:${s < 80 ? "0" + s : s} minutes`;
  };
 

setInterval(countdown, 1000);
