import Api from "@/endpoint/Api";

export default {
  getBySchoolId(schoolId) {
    return Api.get(`school/${schoolId}/invite`);
  },
  add(schoolId, invite) {
    return Api.post(`school/${schoolId}/invite`, invite);
  },
  put(schoolId, invite) {
    return Api.put(`school/${schoolId}/invite/${invite.id}`, invite);
  },
  delete(schoolId, invite) {
    return Api.delete(`school/${schoolId}/invite/${invite.id}`);
  },
  acceptInviteUrl(schoolId, userId, token){
    return `${Api.defaults.baseURL}/school/${schoolId}/invite/accept?userId=${userId}&token=${token}`;
  }

};
