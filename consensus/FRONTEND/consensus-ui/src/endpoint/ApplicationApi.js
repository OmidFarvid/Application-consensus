import Api from "@/endpoint/Api";

export default {
  getBySeasonId(seasonId) {
    return Api.get(`season/${seasonId}/application`);
  },
  add(seasonId, application) {
    return Api.post(`season/${seasonId}/application`, application);
  },
  put(seasonId, application) {
    return Api.put(
      `season/${seasonId}/application/${application.id}`,
      application
    );
  },
  delete(seasonId, application) {
    return Api.delete(`season/${seasonId}/application/${application.id}`);
  },
  uploadCsv(seasonId, formData) {
    return Api.post(`season/${seasonId}/application/upload_csv`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        enctype: "multipart/form-data"
      }
    });
  }
};
