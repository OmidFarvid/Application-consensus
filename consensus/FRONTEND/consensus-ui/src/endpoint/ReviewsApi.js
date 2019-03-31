import Api from "@/endpoint/Api";

export default {
  getByApplicationId(applicationId) {
    return Api.get(`application/${applicationId}/review`);
  },
  add(applicationId, review) {
    return Api.post(`application/${applicationId}/review`, review);
  },
  put(applicationId, review) {
    return Api.put(`application/${applicationId}/review/` + review.id, review);
  },
  delete(applicationId, review) {
    return Api.delete(`application/${applicationId}/review/` + review.id);
  }
};
