
const labels = document.getElementById("time-labels");
const line = document.getElementById("current-time-line");

const HOUR_HEIGHT = 60;

// Tạo các nhãn giờ
for (let hour = 0; hour < 24; hour++) {
    const label = document.createElement("div");
    label.className = "time-label";
    label.textContent = `${String(hour).padStart(2, "0")}:00`;
    labels.appendChild(label);
}

// Cập nhật theo giờ Việt Nam
function updateCurrentTime() {
    const now = new Date();

    const parts = new Intl.DateTimeFormat("en-GB", {
        timeZone: "Asia/Ho_Chi_Minh",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hourCycle: "h23"
    }).formatToParts(now);

    const getPart = type =>
        Number(parts.find(p => p.type === type).value);

    const hour = getPart("hour");
    const minute = getPart("minute");
    const second = getPart("second");

    const top =
        (hour * 60 + minute + second / 60) *
        (HOUR_HEIGHT / 60);

    line.style.top = `${top}px`;
}

updateCurrentTime();
setInterval(updateCurrentTime, 1000);
