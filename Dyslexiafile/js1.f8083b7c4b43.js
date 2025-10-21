const nextDom = document.getElementById("next");
const prevDom = document.getElementById("prev");
const edgeDom = document.querySelector(".edge");
const listItemDom = document.querySelector(".edge .inner");
const thumbnailDom = document.querySelector(".edge .thumbnail");

const timeRunning = 3000;
const timeAutoNext = 7000;

let runTimeout;
let autoRun = setTimeout(() => {
  nextDom.click();
}, timeAutoNext);

nextDom.onclick = () => {
  showSlider("next");
};

prevDom.onclick = () => {
  showSlider("prev");
};

function showSlider(type) {
  const items = document.querySelectorAll(".edge .inner .center");
  const thumbs = document.querySelectorAll(".edge .thumbnail .center");

  if (type === "next") {
    // Move first item to the end
    listItemDom.appendChild(items[0]);
    thumbnailDom.appendChild(thumbs[0]);
    edgeDom.classList.add("next");
  } else if (type === "prev") {
    // Move last item to the beginning
    const lastIndex = items.length - 1;
    listItemDom.prepend(items[lastIndex]);
    thumbnailDom.prepend(thumbs[lastIndex]);
    edgeDom.classList.add("prev");
  }

  // Reset animation classes after animation time
  clearTimeout(runTimeout);
  runTimeout = setTimeout(() => {
    edgeDom.classList.remove("next", "prev");
  }, timeRunning);

  // Reset auto slider timer
  clearTimeout(autoRun);
  autoRun = setTimeout(() => {
    nextDom.click();
  }, timeAutoNext);
}
