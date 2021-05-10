<template>
  <v-row justify="center">
    <v-dialog v-model="show" persistent max-width="500">
      <v-card>
        <v-card-title class="headline">{{ promoData.promoTitle }}</v-card-title>
        <v-card-text>
          <v-container>
            {{ promoData.promoText }}
            <img
              v-if="promoData.promoImg"
              :src="promoData.promoImg"
              alt=""
              style="width: 100%"
            />
            <v-row>
              <v-col cols="12">
                <v-text-field
                  :error-messages="error"
                  v-model="email"
                  label="Email*"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-btn color="grey darken-1" text @click="callback()">
            {{ promoData.skipBtnText }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            :loading="loading"
            color="green darken-1"
            class="white--text"
            @click="dialogAction(true)"
          >
            {{ promoData.submitBtnText }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  props: {
    show: Boolean,
    callback: Function,
    promoData: Object,
  },
  data() {
    return {
      loading: false,
      email: "",
      error: "",
      couponId: "",
      couponText: "",
    };
  },
  computed: {
    metamaskAddress() {
      return this.$store.state.metamaskAddress;
    },
  },
  methods: {
    dialogAction(result) {
      if (result && this.email != "") {
        this.loading = true;
        let _this = this;
        this.$http
          .post(
            this.$HOST +
              "/api/submit/email/" +
              this.email +
              "?address=" +
              this.metamaskAddress,
            JSON.stringify({}),
            { withCredentials: true }
          )
          .then(function (response) {
            console.log(response);
            this.$cookie.set("popup_coupons_uid", response.popup_coupons_uid);
            _this.error = "";
            _this.callback();
          })
          .catch(function (error) {
            console.log(error);
            if (error && error.response.status == 400) {
              _this.error = error.response.data.msg;
            }
          });
        this.loading = false;
      }
    },
  },
  mounted() {},
};
</script>