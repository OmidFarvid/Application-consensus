<template>
  <section class="container-fluid">
    <div class="row row-no-padding justify-content-end">
      <div class="col-md-4 col-sm-4 col-xs-4">
        <button
          class="btn btn-block btn-success"
          @click="showNewApplicationModal()"
        >
          <i class="glyphicon glyphicon-ok"></i> Submit a new application
        </button>
      </div>
    </div>
    <div class="row row-no-padding">
      <div class="col-md-4 col-sm-4 col-xs-12">
        <div
          class="boxing"
          v-on:click="onApplicationBoxClick"
          v-bind:class="{ active: applicationShown }"
        >
          <i class="fa fa-eye"></i>
          <h5>Applications Review</h5>
          <br />
          <div class="info">
            <div class="left">
              <h6>Received : {{ season.application }}</h6>
              <h6>Reviewed : {{ season.applicationReviewed }}</h6>
            </div>
            <div class="right">{{ season.newApplication }} new</div>
          </div>
        </div>
      </div>
      <div class="col-md-4 col-sm-4 col-xs-12">
        <div
          class="boxing"
          v-on:click="onEnrolledBoxClick"
          v-bind:class="{ active: enrolledShown }"
        >
          <i class="fa fa-handshake-o"></i>
          <h4>enrolled</h4>
          <div class="info">
            <div class="left">
              <h6>Student enrolled : {{ season.applicationEnrolled }}</h6>
            </div>
            <div class="right">{{ season.newEnrolled }} new</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Review Application -->
    <div class="row row-no-padding" v-if="applicationShown">
      <vuetable
        ref="vuetable"
        :api-mode="false"
        :data="notEnrolledData"
        :fields="tableFields"
        :css="css.table"
        class="application-table"
        :query-params="{
          sort: 'order_by',
          page: 'page',
          perPage: 'page_size'
        }"
        data-path="results"
        pagination-path="pagination"
        @vuetable:pagination-data="onPaginationData"
      >
        <template slot="review_actions" scope="props">
          <div class="table-button-container">
            <button
              class="btn btn-warning btn-sm"
              @click="showReviewModal(props.rowData)"
            >
              <span class="glyphicon glyphicon-pencil"></span></button
            >&nbsp;&nbsp;
          </div>
        </template>
        <template slot="decision_actions" scope="props">
          <div class="table-button-container">
            <button
              class="btn btn-success btn-sm"
              @click="showAcceptConfirmation(props.rowData)"
            >
              <span class="glyphicon glyphicon-check"></span></button
            >&nbsp;&nbsp;
            <button
              class="btn btn-outline-danger btn-sm"
              @click="showRejectConfirmation(props.rowData)"
            >
              <span class="glyphicon glyphicon-trash"></span></button
            >&nbsp;&nbsp;
          </div>
        </template>
      </vuetable>
    </div>
    <!-- End Review Application -->

    <!-- Enrolled Application -->
    <div class="row row-no-padding" v-if="enrolledShown">
      <vuetable
        ref="vuetable"
        :api-mode="false"
        :data="enrolledData"
        :fields="tableFields"
        :css="css.table"
        class="application-table"
        :query-params="{
          sort: 'order_by',
          page: 'page',
          perPage: 'page_size'
        }"
        data-path="results"
        pagination-path="pagination"
        @vuetable:pagination-data="onPaginationData"
      >
        <template slot="review_actions" scope="props">
          <div class="table-button-container">
            <button
              class="btn btn-warning btn-sm"
              @click="scoreBoxClick(props.rowData)"
            >
              <span class="fa fa-eye"></span>
            </button>
          </div>
        </template>
      </vuetable>
    </div>
    <!-- End Enrolled Application -->

    <!-- New Application Modal-->
    <b-modal
      size="lg"
      centered
      ref="newApplicationModalRef"
      id="newAModal"
      title="Add a new application"
      :header-bg-variant="'modal-header padding-10 background-light-silver'"
      :footer-bg-variant="
        'modal-footer padding-10 background-light-silver border-bottom-right-radius-10 border-bottom-left-radius-10'
      "
      :aria-required="false"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-body">
            <form>
              <div class="row">
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">First Name</label>
                    <input
                      type="text"
                      class="form-control"
                      v-model="selectedApplication.first_name"
                    />
                  </div>
                </div>
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Last Name</label>
                    <input
                      type="text"
                      class="form-control"
                      v-model="selectedApplication.last_name"
                    />
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Birthday</label>
                    <dateTime
                      v-model="selectedApplication.date_of_birth"
                    ></dateTime>
                  </div>
                </div>
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Gender</label>
                    <select
                      class="form-control"
                      v-model="selectedApplication.gender"
                    >
                      <option value="m">Male</option>
                      <option value="f">Female</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Email</label>
                    <input
                      type="email"
                      class="form-control"
                      v-model="selectedApplication.email"
                    />
                  </div>
                </div>
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Phone Number</label>
                    <input
                      type="text"
                      class="form-control"
                      v-model="selectedApplication.phone_number"
                    />
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Info</label>
                    <textarea
                      class="form-control"
                      v-model="selectedApplication.info"
                    ></textarea>
                  </div>
                </div>
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <div class="form-group">
                    <label class="pull-left">Educational Info</label>
                    <textarea
                      class="form-control"
                      v-model="selectedApplication.educational_info"
                    ></textarea>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div slot="modal-footer" class="w-100">
        <div class="row row-no-padding width-full">
          <div class="col-md-4 col-sm-4 col-xs-12">
            <button
              v-on:click="submitApplication"
              type="button"
              class="btn btn-success btn-block"
            >
              <i class="glyphicon glyphicon-ok"></i> Add Application
            </button>
          </div>
          <div class="col-md-3 col-sm-3 col-xs-12">
            <button
              type="button"
              class="btn btn-danger btn-block"
              data-dismiss="modal"
              @click="$refs.newApplicationModalRef.hide()"
            >
              <i class="fa fa-close"></i> Cancel
            </button>
          </div>
        </div>
      </div>
    </b-modal>

    <!-- Confirmation Modal-->
    <b-modal
      centered
      ref="confirmModalRef"
      id="confirmModal"
      :hide-header="true"
    >
      <p v-if="rejectConfirm" class="text-danger h6">
        Are you sure to reject this application?
      </p>
      <p v-if="acceptConfirm" class="text-danger h6">
        Are you sure to accept this application?
      </p>
      <div slot="modal-footer" class="w-100">
        <button
          type="button"
          class="btn btn-secondary float-left"
          @click="$refs.confirmModalRef.hide()"
        >
          <i class="la la-close"></i> Cancel
        </button>
        <button
          v-if="rejectConfirm"
          type="button"
          class="btn btn-danger float-right"
          @click="rejectApplication()"
        >
          <span v-show="rejectApplication">reject</span>
        </button>
        <button
          v-if="acceptConfirm"
          type="button"
          class="btn btn-success float-right"
          @click="acceptApplication()"
        >
          <span v-show="acceptApplication">Accept</span>
        </button>
      </div>
    </b-modal>

    <!-- Review Modal-->
    <b-modal
      size="lg"
      centered
      ref="reviewAppModalRef"
      id="reviewAppModal"
      :title="
        'Review ' +
          selectedApplication.first_name +
          ' ' +
          selectedApplication.last_name +
          ' application'
      "
      :header-bg-variant="'modal-header padding-10 background-light-silver'"
      :footer-bg-variant="
        'modal-footer padding-10 background-light-silver border-bottom-right-radius-10 border-bottom-left-radius-10'
      "
      :aria-required="false"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-body">
            <form>
              <div class="rounded main_body">
                <div class="row">
                  <div class="col-md-4 text-left">
                    <span>info</span>
                  </div>
                  <div class="col-md-4 text-left">
                    <span>Educational Info</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4 text-left">
                    <textarea
                      class="border-dark form-control"
                      rows="5"
                      v-model="selectedReview.info"
                    ></textarea>
                  </div>
                  <div class="col-md-4 text-left">
                    <textarea
                      class="border-dark form-control"
                      rows="5"
                      v-model="selectedReview.educationalInfo"
                    ></textarea>
                  </div>
                </div>
                <br />
                <div class="row">
                  <div class="col-md-4 text-left">
                    <span>Who has reviewed:</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-12">
                    <vuetable
                      ref="vuetable"
                      :api-mode="false"
                      :data="reviewData"
                      :fields="reviewTableFields"
                      :css="css.table"
                      class="application-table"
                    >
                    </vuetable>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4 text-left">
                    <span>Do Review this Application</span>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 text-left">
                    <span
                      v-for="score in scores"
                      v-bind:key="score"
                      class="scores"
                      v-on:click="selectScore(score)"
                    >
                      {{ score }} <span class="review_divider">|</span></span
                    >
                  </div>
                  <div class="col-md-2 left-text">
                    <input
                      type="number"
                      name="txtReview"
                      id="txtReviewScore"
                      class="form-control border-dark text-right"
                      v-model="selectedReview.score"
                    />
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4 text-left">
                    Review Note:
                  </div>
                </div>
                <div class="row">
                  <div
                    class="col-lg-10 col-md-10 col-sm-10 col-xs-10 col-xl-10 text-left"
                  >
                    <textarea
                      name="txtReview"
                      id="txtReviewNote"
                      cols="30"
                      rows="2"
                      class="form-control border-dark"
                      v-model="selectedReview.note"
                    ></textarea>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div slot="modal-footer" class="w-100">
        <div class="row row-no-padding width-full">
          <div class="col-md-4 col-sm-4 col-xs-12">
            <button
              v-on:click="submitReview"
              type="button"
              class="btn btn-success btn-block"
            >
              <i class="glyphicon glyphicon-ok"></i>Submit Review
            </button>
          </div>
          <div class="col-md-3 col-sm-3 col-xs-12">
            <button
              type="button"
              class="btn btn-danger btn-block"
              data-dismiss="modal"
              @click="$refs.reviewAppModalRef.hide()"
            >
              <i class="fa fa-close"></i> Cancel
            </button>
          </div>
        </div>
      </div>
    </b-modal>
  </section>
</template>

<script>
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePagination from "vuetable-2/src/components/VuetablePagination";
import bModal from "bootstrap-vue/es/components/modal/modal";
import utilMixin from "@/mixins/UtilMixin";
import vuetableBootstrapMixin from "../../../mixins/VuetableBootstrapMixin";
import applicationApi from "../../../endpoint/ApplicationApi";
import ApplicationStatus from "../model/ApplicationStatus";
import dateTime from "../../dateTimePicker/DateTimePicker";
import ReviewsApi from "../../../endpoint/ReviewsApi";

let reviewActionField = {
  name: "__slot:review_actions",
  title: "review",
  titleClass: "text-left"
};
let decisionActionField = {
  name: "__slot:decision_actions",
  title: "decision",
  titleClass: "text-left"
};

export default {
  name: "SeasonHome",
  mixins: [utilMixin, vuetableBootstrapMixin],
  components: {
    Vuetable,
    dateTime,
    VuetablePagination,
    "b-modal": bModal
  },
  created: function() {
    this.$eventsBus.$emit("header:title", "School's season");
    this.schoolId = +this.$route.params.school_id;
    this.seasonId = +this.$route.params.season_id;
    this.reAssignData();
  },
  data: function() {
    return {
      schoolId: 0,
      seasonId: 0,
      season: {
        application: 0,
        applicationReviewed: 0,
        applicationEnrolled: 0,
        newEnrolled: 0,
        newApplication: 0
      },
      scores: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
      selectedReview: {},
      selectedApplication: {},
      applicationShown: false,
      enrolledShown: false,
      rejectConfirm: false,
      acceptConfirm: false,
      seasonData: {},
      enrolledData: [],
      notEnrolledData: [],
      reviewActionField: reviewActionField,
      decisionActionField: decisionActionField,
      reviewData: [],
      reviewTableFields: [
        {
          name: "reviewer_full_name",
          title: "Reviewer",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "review_date",
          sortField: "review_date",
          title: "Date",
          titleClass: "text-left",
          dataClass: "text-left"
        }
      ],
      tableFields: [
        {
          sortField: "first_name",
          name: "first_name",
          title: "First Name",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "last_name",
          title: "Last Name",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "date_of_birth",
          title: "Date of birth",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "gender",
          title: "Gender",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "email",
          title: "Email",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "phone_number",
          title: "Phone number",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "info",
          title: "Info",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "educational_info",
          title: "Educational Info",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "review",
          title: "Review",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "status",
          title: "Status",
          titleClass: "text-left",
          dataClass: "text-left"
        },
        reviewActionField,
        decisionActionField
      ]
    };
  },
  methods: {
    showNewApplicationModal: function() {
      this.selectedApplication = {};
      this.$refs.newApplicationModalRef.show();
    },
    reAssignData: function() {
      let self = this;
      self.enrolledData = [];
      self.notEnrolledData = [];
      self.reviewData = [];
      self.season.applicationReviewed = 0;
      self.season.applicationEnrolled = 0;
      self.season.newApplication = 0;
      self.season.newEnrolled = 0;
      applicationApi.getBySeasonId(this.seasonId).then(
        function(response) {
          self.seasonData = response.data;
          self.fragmentationApplication(response.data.results);
        },
        function(resp) {
          self.notifyError(
            (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to get application"
          );
        }
      );
    },
    fragmentationApplication: function(applications) {
      let self = this;
      this.season.application = applications.length;
      self.season.applicationReviewed = self.season.applicationReviewed || 0;
      applications.forEach(function(application) {
        switch (application.status) {
          case ApplicationStatus.Reviewed:
            self.season.applicationReviewed++;
            self.notEnrolledData.push(application);
            break;
          case ApplicationStatus.Enrolled:
            self.season.applicationEnrolled++;
            self.enrolledData.push(application);
            break;
          default:
            self.notEnrolledData.push(application);
        }

        // Count new(today) applications
        if (
          self.formatDate(application.created_date, "YYYY/MM/DD") ===
          self.formatDate(new Date(), "YYYY/MM/DD")
        ) {
          switch (application.status) {
            case ApplicationStatus.Enrolled:
              self.season.newEnrolled++;
              break;
            case ApplicationStatus.Reviewed:
            case ApplicationStatus.Pending:
              self.season.newApplication++;
              break;
          }
        }
      });
    },
    onEnrolledBoxClick: function() {
      this.enrolledShown = !this.enrolledShown;
      this.applicationShown = false;
      this.decisionActionField.visible = !this.enrolledShown;
      this.$refs.vuetable && this.$refs.vuetable.normalizeFields();
    },
    onApplicationBoxClick: function() {
      this.applicationShown = !this.applicationShown;
      this.enrolledShown = false;
      this.decisionActionField.visible = this.applicationShown;
      this.$refs.vuetable && this.$refs.vuetable.normalizeFields();
    },
    submitApplication: function() {
      let self = this;
      self.selectedApplication.season = self.seasonId;
      applicationApi.add(this.seasonId, self.selectedApplication).then(
        function() {
          self.notifySuccess("The application inserted");
          self.$refs.newApplicationModalRef.hide();
          self.reAssignData();
        },
        function(resp) {
          self.notifyError(
            (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to add the new application"
          );
        }
      );
    },
    showRejectConfirmation: function(application) {
      this.rejectConfirm = true;
      this.acceptConfirm = false;

      this.selectedApplication = application;
      this.$refs.confirmModalRef.show();
    },
    showAcceptConfirmation: function(application) {
      this.acceptConfirm = true;
      this.rejectConfirm = false;

      this.selectedApplication = application;
      this.$refs.confirmModalRef.show();
    },
    acceptApplication: function() {
      let self = this;
      this.selectedApplication.status = "enrolled";
      applicationApi.put(this.seasonId, this.selectedApplication).then(
        function() {
          self.notifySuccess("The application accepted");
          self.$refs.confirmModalRef.hide();
          self.reAssignData();
        },
        function(resp) {
          self.notifyError(
            (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to accept the application"
          );
        }
      );
    },
    rejectApplication: function() {
      let self = this;
      this.selectedApplication.status = "reject";
      applicationApi.put(this.seasonId, this.selectedApplication).then(
        function() {
          self.notifySuccess("The application rejected");
          self.$refs.confirmModalRef.hide();
          self.$refs.vuetable.refresh();
        },
        function(resp) {
          self.notifyError(
            (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to reject the application"
          );
        }
      );
    },
    showReviewModal: function(application) {
      let self = this;
      self.selectedReview = {};
      // Get current application's reviews
      ReviewsApi.getByApplicationId(application.id).then(
        function(resp) {
          self.selectedApplication = application;
          self.reviewData = resp.data;
          // If the user already reviewed the application
          let reviews = self.reviewData.filter(function(review) {
            if (review.user === self.$store.state.currentUser.id) {
              return review;
            }
          });
          if (reviews.length > 0) {
            self.selectedReview = reviews[0];
          }
          self.$refs.reviewAppModalRef.show();
        },
        function(resp) {
          self.notifyError(
            (resp.response && resp.response.data.detail) ||
              "Some error happened when trying to get reviewers"
          );
        }
      );
    },
    selectScore: function(score) {
      this.$set(this.selectedReview, "score", score);
    },
    submitReview: function() {
      let self = this;
      if (!this.selectedReview.id) {
        this.selectedReview.application = this.selectedApplication.id;
        ReviewsApi.add(this.selectedApplication.id, this.selectedReview).then(
          function() {
            self.notifySuccess("The review submitted");
            self.reAssignData();
            self.$refs.reviewAppModalRef.hide();
          },
          function(resp) {
            self.notifyError(
              (resp.response && resp.response.data.detail) ||
                "Some error happened when trying to add the review"
            );
          }
        );
      } else {
        ReviewsApi.put(this.selectedApplication.id, this.selectedReview).then(
          function() {
            self.notifySuccess("The review updated");
            self.$refs.reviewAppModalRef.hide();
          },
          function(resp) {
            self.notifyError(
              (resp.response && resp.response.data.detail) ||
                "Some error happened when trying to add the review"
            );
          }
        );
      }
    }
  }
};
</script>

<style>
.application-table {
  margin-top: 15px;
  margin-left: 15px;
  margin-right: 15px;
}

span.scores {
  color: blue;
  cursor: pointer;
}

.scores:last-of-type .review_divider {
  display: none;
}

input[type="number"]::-webkit-inner-spin-button {
  margin-left: 10px;
}
</style>
