<template>
    <div class="rate">
        <div class="container">
            <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-xs-12 offset-2 outer_div boder1">
                <div class="text-left boder1">
                    Review Application
                    <br/>
                </div>
                <div class="rate-form">
                    <div class="row">
                        <div class="col-md-2">
                            <img src="" alt="Avatar" class="img-rounded"/>
                        </div>
                        <div class="col-md-2 text-left">
                            <h6>{{application.name}}</h6>
                        </div>
                    </div>
                    <div class="rounded main_body">
                        <div class="row">
                            <div class="col-md-4 text-left offset-1">
                                <span>info</span>
                            </div>
                            <div class="col-md-4 text-left offset-2">
                                <span>Educational Info</span>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-4 text-left offset-1">
                                <textarea class="border-dark form-control" rows="5"></textarea>
                            </div>
                            <div class="col-md-4 text-left offset-2">
                                <textarea class="border-dark form-control" rows="5"></textarea>
                            </div>
                        </div>
                        <br>
                        <br>
                        <div class="row">
                            <div class="col-md-4 text-left offset-1">
                                <span>Do Score this Application</span>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6 text-left offset-1">
                    <span v-for="rate in rates" v-bind:key="rate" class="rates">
                        {{rate}} <span class="rate_divider">|</span></span>
                            </div>
                            <div class="col-md-2 left-text">
                                <input type="number" name="txtRate" id="txtRate"
                                       class="form-control border-dark text-right">
                            </div>
                        </div>
                        <br/>
                        <div class="row">
                            <div class="col-md-4 offset-1 text-left">
                                Review Note:
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-10 col-md-10 col-sm-10 col-xs-10 col-xl-10 offset-1 text-left">
                            <textarea name="txtReview" id="txtReview" cols="30" rows="2"
                                      class="form-control border-dark"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-8 col-lg-8 col-md-8 col-sm-12 col-xs-12 offset-2 footer_div boder1">
                <div class="row">
                    <div class="col-md-4">
                        <input type="button" class="btn btn-lg btn-block btn-success" value="Rate"/>
                    </div>
                    <div class="col-md-2">
                        <input type="button" class="btn btn-lg btn-block btn-danger" value="cancel"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import UtilMixin from "@/mixins/UtilMixin";
    import ApplicationApi from "../../endpoint/ApplicationApi";

    export default {
        name: "Rate",
        mixins: [UtilMixin],
        created: function(){
            this.getApplication();
            this.schoolId = +this.$route.params.school_id;
            this.seasonId = +this.$route.params.season_id;
            this.applicationId = +this.$route.params.application_id;
        },
        data() {
            return {
                rates: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                schoolId: 0,
                seasonId: 0,
                applicationId: 0,
            }

        },
        methods: {
            getApplication: function () {
                let self = this;
                ApplicationApi.get(this.schoolId).then(function (response) {
                    self.application = response.data;
                    alert(self.application.id)
                });
            },
        }
    };
</script>

<style scoped>

    .rate {
        background-color: #fff !important;
    }

    span.rates {
        color: blue;
        cursor: pointer;
    }

    .rates:last-child {
        #display: none;
    }

    .main_body {
        border: 2px solid black;
        padding-top: 30px;
        padding-bottom: 30px;
        border-radius: 20px !important;
        margin-right: 20px;
        margin-left: 20px;
    }

    .outer_div {
        padding-bottom: 20px;
        padding-right: 0px;
        padding-left: 0px;
    }

    .footer_div {
        background-color: #bbbbbb;
        padding-top: 15px;
        padding-bottom: 30px;
    }

    .rates:last-of-type .rate_divider {
        display: none;
    }

    .boder1 {
        border: 1px solid black;
    }

    input[type=number]::-webkit-inner-spin-button {
        margin-left: 10px;
    }
</style>