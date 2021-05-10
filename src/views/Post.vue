<template>
  <div>
    <v-progress-circular
      v-if="loading"
      indeterminate
      color="primary"
    ></v-progress-circular>
    <div v-if="htmlContent">
      <div v-html="htmlContent.data"></div>
      <v-btn class="mr-1" @click="buyForXYR(htmlContent.xyr)"
        >{{ htmlContent.xyr }} XYR</v-btn
      >
      <v-btn class="ml-1" @click="buyForETH(htmlContent.eth)"
        >{{ htmlContent.eth }} ETH</v-btn
      >
    </div>
    <PromoDialog :show="dialog" :callback="dialogAction" :promoData="form" />
  </div>
</template>

<script>
const IPFS = require("ipfs-mini");
const ipfs = new IPFS({
  host: "ipfs.infura.io",
  port: 5001,
  protocol: "https",
});
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
      htmlContent: null,
      loading: false,
    };
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
    readIPFS(post) {
      if (post.key != "") {
        this.loading = true;
        ipfs.cat(post.key, (err, result) => {
          if (result) {
            this.htmlContent = {
              data: result,
              created: post.created,
              key: post.key,
              category: post.category,
              img: post.img,
              xyr: post.xyr,
              eth: post.eth,
            };
          }
          this.loading = false;
        });
      }
    },
    getPost(key) {
      this.loading = true;
      this.$http
        .get(this.$HOST + "/api/get/content/" + key, {
          withCredentials: true,
        })
        .then((resp) => {
          this.selectedItem = resp.data;
          this.readIPFS(this.selectedItem);
        })
        .catch((error) => {
          console.log(error);
          this.loading = false;
        });
    },
  },
  watch: {
    $route() {},
  },
  mounted() {
    const key = this.$route.params.key;
    this.getPost(key);
    this.loadData()
  },
};
</script>