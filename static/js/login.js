window.onload = () => {
  console.log("로그인 페이지");
};

const loginBtn = document.getElementById("login-btn");
const tokenLoginBtn = document.getElementById("token-login-btn");

const onClickLogin = async () => {
  console.log("로그인 버튼 클릭");
  const email = document.getElementById("email");
  const password = document.getElementById("password");

  const json = await (
    await fetch("http://127.0.0.1:8000/api/token/", {
      headers: { "content-type": "application/json" },
      method: "POST",
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    })
  ).json();

  // 토큰을 얻었다면 이를 로컬 스토리지에 저장한다.
  const base64url = json.access.split(".")[1];
  const base64 = base64url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(
    atob(base64)
      .split("")
      .map((c) => {
        return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
      })
      .join("")
  );

  localStorage.setItem("access", json.access);
  localStorage.setItem("refresh", json.refresh);
  localStorage.setItem("payload", jsonPayload);
};

const onClickTokenLogin = async () => {
  console.log("토큰 로그인 버튼 클릭");

  const json = await (
    await fetch("http://127.0.0.1:8000/api/v1/users/1", {
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access"),
      },
    })
  ).json();
};

loginBtn.addEventListener("click", onClickLogin);
tokenLoginBtn.addEventListener("click", onClickTokenLogin);
