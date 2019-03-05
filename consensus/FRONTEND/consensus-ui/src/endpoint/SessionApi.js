import Api from "@/endpoint/Api";

export default {
  getUser() {
    return Api.get("session");
  },
  login(username, password) {
    return Api.post("session", { username: username, password: password });
  },
  signUp(fields) {
    return Api.post("session/signup", fields);
  },
  logout() {
    return Api.delete("session");
  }
};
