window.onload = () => {
  console.log("홈 페이지");
  console.log(localStorage.getItem("access"));

  const payload = localStorage.getItem("payload");
  const parsed_payload = JSON.parse(payload);

  const container = document.getElementById("container");
  const h3 = document.createElement("h3");

  h3.innerText = parsed_payload.email;
  container.appendChild(h3);
};

const logoutBtn = document.getElementById("logout-btn");

const onClickLogout = () => {
  console.log("로그아웃 버튼 클릭");
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  localStorage.removeItem("payload");

  window.location.reload();
};

logoutBtn.addEventListener("click", onClickLogout);
