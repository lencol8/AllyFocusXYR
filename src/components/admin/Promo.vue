<template>
  <v-container fluid>
    <v-sheet elevation="12" class="pa-5 mt-4">
      <v-text-field outlined dense v-model="form.promoTitle" type="text" autocomplete="off" label="Promo title"></v-text-field>
      <v-text-field outlined dense v-model="form.promoImg" type="text" autocomplete="off" label="Promo image URL/Base64"></v-text-field>
      <v-text-field outlined dense v-model="form.promoText" type="text" autocomplete="off" label="Promo text"></v-text-field>
      <v-text-field outlined dense v-model="form.skipBtnText" type="text" autocomplete="off" label="Skip button text"></v-text-field>
      <v-text-field outlined dense v-model="form.submitBtnText" type="text" autocomplete="off" label="Submit button text"></v-text-field>
      <v-btn outlined :loading="loading" @click="dialog = true" color="primary" class="mr-5">Test</v-btn>
      <v-btn :loading="loading" @click="post" color="primary">POST</v-btn>
    </v-sheet>
    <PromoDialog :show="dialog" :callback="dialogAction" :promoData="form"/>
  </v-container>
</template>

<script>

import PromoDialog from "@/components/PromoDialog.vue";

export default {
  components: {
    PromoDialog
  },
  data: () => ({
    loading: false,
    dialog: false,
    form: {
      promoTitle: 'Promo title',
      promoImg: 'Promo image',
      promoText: 'Promo text',
      skipBtnText: 'Skip button text',
      submitBtnText: 'Submit button text',
    }
  }),
  watch: {},
  methods: {
    post() {
      this.loading = true;
      this.$http.post(
        this.$HOST + "/api/set/static" + "?uid=" + this.$cookie.get("uid"),
        JSON.stringify({ key: "coupon_popup", val: this.form }),
        { withCredentials: true }
      );
      this.loading = false;
    },
    dialogAction() {
      this.dialog = false;
    },
    loadData() {
      this.$http
        .get(this.$HOST + "/api/get/static/coupon_popup", {
          withCredentials: true,
        })
        .then((resp) => {
          this.form = resp.data.val;
        });
    },
  },
  mounted() {
    this.loadData()
  },
};
</script>