<template>
  <section>
    <div class="row row-no-padding justify-content-end">
      <div class="col-md-4 col-sm-4 col-xs-4 ">
        <button class="btn btn-block btn-primary" @click="addInvite">
          <i class="fa fa-plus"></i> Add a new Invitation
        </button>
      </div>
    </div>
    <div class="row row-no-padding">
      <div class="col-md-4 justify-content-start">
        <div
          class="boxing"
          v-on:click="inviteShown = !inviteShown"
          v-bind:class="{ active: inviteShown }"
        >
          <i class="fa fa-users"></i>
          <h4>Invites</h4>
          <div class="info">
            <div class="left">
              <h6>
                School invites :
                {{ inviteData.results ? inviteData.results.length : 0 }}
              </h6>
            </div>
            <div class="right"></div>
          </div>
        </div>
      </div>
    </div>
    <div class="row row-no-padding" v-if="inviteShown">
      <vuetable
        ref="vuetable"
        :api-mode="false"
        :data="inviteData"
        :fields="tableFields"
        :css="css.table"
        class="invite-table"
        :query-params="{
          sort: 'order_by',
          page: 'page',
          perPage: 'page_size'
        }"
        data-path="results"
        pagination-path="pagination"
        @vuetable:pagination-data="onPaginationData"
      >
        <template slot="actions" scope="props">
          <div class="table-button-container">
            <button
              class="btn btn-warning btn-sm"
              @click="editRow(props.rowData)"
            >
              <span class="glyphicon glyphicon-pencil"></span> Edit</button
            >&nbsp;&nbsp;
            <button
              class="btn btn-danger btn-sm"
              @click="showConfirmDeleteModal(props.rowData)"
            >
              <span class="glyphicon glyphicon-trash"></span> Delete</button
            >&nbsp;&nbsp;
          </div>
        </template>
      </vuetable>
    </div>
    <b-modal
      size="lg"
      centered
      ref="inviteModalRef"
      id="InviteModal"
      title="Add invite"
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
                  <label>Search and add by username</label>
                  <div class="input-group mb-2">
                    <div class="input-group-prepend">
                      <div class="input-group-text">
                        <i class="fa fa-search"></i>
                      </div>
                    </div>
                    <input
                      type="text"
                      class="form-control"
                      v-model="selectedInvite.username"
                    />
                  </div>
                </div>
                <div class="col-md-6 col-sm-6 col-xs-6">
                  <label> Or search and add by email</label>
                  <div class="input-group mb-2">
                    <div class="input-group-prepend">
                      <div class="input-group-text">
                        <i class="fa fa-search"></i>
                      </div>
                    </div>
                    <input
                      type="text"
                      class="form-control"
                      v-model="selectedInvite.email"
                    />
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
              v-on:click="inviteInvite"
              type="button"
              class="btn btn-success btn-block"
            >
              <i class="glyphicon glyphicon-ok"></i>
              Submit Invite
            </button>
          </div>
          <div class="col-md-3 col-sm-3 col-xs-12">
            <button
              type="button"
              class="btn btn-danger btn-block"
              data-dismiss="modal"
              @click="$refs.inviteModalRef.hide()"
            >
              <i class="fa fa-close"></i> Cancel
            </button>
          </div>
        </div>
      </div>
    </b-modal>
    <b-modal
      centered
      ref="confirmDeleteModalRef"
      id="confirmDeleteModal"
      :hide-header="true"
    >
      <p class="text-danger h6">Are you sure to delete this record?</p>
      <div slot="modal-footer" class="w-100">
        <button
          type="button"
          class="btn btn-secondary float-left"
          @click="$refs.confirmDeleteModalRef.hide()"
        >
          <i class="la la-close"></i> Cancel
        </button>
        <button
          type="button"
          class="btn btn-danger float-right"
          :disabled="deletingRecord"
          @click="deleteInvite()"
        >
          <i
            :class="deletingRecord ? 'la la-spin la-spinner' : 'la la-trash'"
          ></i>
          <span v-show="!deletingRecord">Delete</span>
          <span v-show="deletingRecord">Deleting</span>
        </button>
      </div>
    </b-modal>
  </section>
</template>

<script>
import inviteApi from "../../endpoint/InviteApi";
import Vuetable from "vuetable-2/src/components/Vuetable";
import VuetablePagination from "vuetable-2/src/components/VuetablePagination";
import bModal from "bootstrap-vue/es/components/modal/modal";
import utilMixin from "@/mixins/UtilMixin";
import vuetableBootstrapMixin from "../../mixins/VuetableBootstrapMixin";

export default {
  name: "SchoolInvite",
  mixins: [utilMixin, vuetableBootstrapMixin],
  components: {
    Vuetable,
    VuetablePagination,
    "b-modal": bModal
  },
  props: {
    schoolId: {
      required: true
    }
  },
  created: function() {
    let self = this;
    inviteApi.getBySchoolId(self.schoolId).then(function(response) {
      self.inviteData = response.data;
    });
  },
  data: function() {
    return {
      inviteData: {},
      tableFields: [
        {
          sortField: "first_name",
          name: "first_name",
          title: `<span class="icon is-small orange"><i class="fa fa-book color-gray"></i></span> First Name`,
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "last_name",
          title: `<span class="icon is-small orange"><i class="fa fa-users color-gray"></i></span> Last Name`,
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "email",
          title: `<span class="icon is-small orange"><i class="fa fa-calendar color-gray"></i></span> Email`,
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "phone_number",
          title: `<span class="icon is-small orange"><i class="fa fa-send color-gray"></i></span> Phone Number`,
          titleClass: "text-left",
          dataClass: "text-left"
        },
        {
          name: "user_name",
          title: `<span class="icon is-small orange"><i class="fa fa-calendar color-gray"></i></span> User Name`,
          titleClass: "text-left",
          dataClass: "text-left"
        },
        "__slot:actions"
      ],
      selectedInvite: {},
      deletingRecord: false,
      inviteShown: false
    };
  },
  methods: {
    showConfirmDeleteModal: function(invite) {
      this.selectedInvite = invite;
      this.$refs.confirmDeleteModalRef.show();
    },
    deleteInvite: function() {
      let self = this;
      self.deletingRecord = true;

      inviteApi.delete(self.schoolId, self.selectedInvite).then(
        function() {
          self.$refs.vuetable.refresh();
          self.deletingRecord = false;
          self.$refs.confirmDeleteModalRef.hide();
          self.inviteData.results.splice(
            self.inviteData.result.indexOf(self.selectedInvite)
          );
          self.notifySuccess("The invite deleted");
        },
        function() {
          self.deletingRecord = false;
          self.notifyError(
            "Some error happened when trying to delete the invite"
          );
        }
      );
    },
    editRow: function(invite) {
      this.selectedInvite = invite;
      this.$refs.inviteModalRef.show();
    },
    addInvite: function() {
      this.selectedInvite = {};
      this.$refs.inviteModalRef.show();
    },
    inviteInvite: function() {
      let self = this;
      inviteApi.add(self.schoolId, self.selectedInvite).then(
        function(resp) {
          if (resp.data.Message !== undefined) {
            if (resp.data.success === "true") {
              self.notifySuccess(resp.data.Message);
            } else {
              self.notifyError(resp.data.Message);
            }
          } else {
            self.notifySuccess("The invite invited");
          }
          self.$refs.inviteModalRef.hide();
          self.inviteData.results.push(resp.data);
        },
        function(Message) {
          console.log(Message);
          self.notifyError(
            "Some error happened when trying to add the new invite"
          );
        }
      );
    }
  }
};
</script>

<style>
.invite-table {
  margin-top: 15px;
  margin-left: 15px;
  margin-right: 15px;
}
</style>
