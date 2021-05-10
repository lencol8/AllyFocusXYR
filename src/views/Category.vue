<template>
  <v-container class="pt-0">
    <v-text-field
      v-model="search"
      append-icon="mdi-magnify"
      label="Search"
      single-line
    ></v-text-field>
    <v-row justify="center">
      <v-col cols="12" class="pt-0">
        <v-row v-if="content.length > 0">
          <v-col md="4" sm="12" v-for="post in content" :key="post.key">
            <v-card class="mx-auto" min-width="344">
              <router-link
                :to="{
                  name: 'Post',
                  params: {
                    city: post.city,
                    category: post.category,
                    key: post.key,
                  },
                }"
              >
                <v-img :src="post.img" height="200px" contain></v-img>
              </router-link>

              <v-card-title>
                <router-link
                  :to="{
                    name: 'Post',
                    params: {
                      city: post.city,
                      category: post.category,
                      key: post.key,
                    },
                  }"
                  >{{ post.title }}</router-link
                >
              </v-card-title>

              <v-card-actions>
                <v-btn color="red" text @click="buyForXYR(post.xyr)"
                  >{{ post.xyr }} XYR</v-btn
                >
                <v-btn color="primary" text @click="buyForETH(post.eth)"
                  >{{ post.eth }} ETH</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>

        <v-progress-circular
          v-if="loading"
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-col>
    </v-row>

    <PromoDialog :show="dialog" :callback="dialogAction" :promoData="form" />
  </v-container>
</template>

<script>
import PromoDialog from "@/components/PromoDialog.vue";
export default {
  components: {
    PromoDialog,
  },
  data() {
    return {
      dialog: false,
      form: {
        promoTitle: "Promo title",
        promoImg: "Promo image",
        promoText: "Promo text",
        skipBtnText: "Skip button text",
        submitBtnText: "Submit button text",
      },
      content: [],
      loading: false,
      search: "",
      searchTimer: null,
    };
  },
  watch: {
    search(newValue) {
      const city = this.$route.params.city;
      const category = this.$route.params.category;
      if (this.searchTimer) {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(
        this.getContent,
        350,
        city,
        category,
        newValue
      );
    },
  },
  computed: {
    contractABI() {
      return this.$store.state.contractABI;
    },
    tokenAddress() {
      return this.$store.state.tokenAddress;
    },
    metamaskAddress() {
      return this.$store.state.metamaskAddress;
    },
  },
  methods: {
    loadData() {
      this.$http
        .get(this.$HOST + "/api/get/static/coupon_popup", {
          withCredentials: true,
        })
        .then((resp) => {
          this.form = resp.data.val;
        });
    },
    showPromoIfNotUID() {
      if (this.$cookie.get("popup_coupons_uid")) return;
      this.dialog = true;
    },
    dialogAction() {
      this.dialog = false;
    },
    gasPrice() {
      return window.web3.utils.toWei(this.$store.state.gasPrice, "gwei");
    },
    async buyForETH(amount) {
      this.showPromoIfNotUID();
      window.web3.eth.sendTransaction(
        {
          from: this.metamaskAddress,
          to: this.tokenAddress,
          value: window.web3.utils.toWei(amount),
          // gasPrice: this.gasPrice(),
          gas: "90000",
        },
        function (err, transactionHash) {
          if (!err) console.log(transactionHash + " success");
        }
      );
    },
    async buyForXYR(amount) {
      this.showPromoIfNotUID();
      let contract = new window.web3.eth.Contract(
        this.contractABI,
        this.tokenAddress,
        {
          from: this.metamaskAddress,
        }
      );
      let v = await contract.methods
        .transfer(this.tokenAddress, window.web3.utils.toWei(amount))
        .send({
          gas: '90000',
          // gasPrice: this.gasPrice()
        });
      console.log(v);
    },
    getContent(city, category, search) {
      this.loading = true;
      search = search != null ? search : "";
      this.$http
        .get(
          this.$HOST +
            "/api/search/content?args=" +
            JSON.stringify({ city: city, category: category }) +
            "&search=" +
            search,
          { withCredentials: true }
        )
        .then((resp) => {
          this.content = resp.data;
          this.loading = false;
        })
        .catch((error) => {
          console.log(error);
          this.loading = false;
        });
    },
  },
  mounted() {
    const city = this.$route.params.city;
    const category = this.$route.params.category;
    this.getContent(city, category);
    this.loadData()
  },
};
</script>