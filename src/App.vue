<template>
  <v-app :style="{ backgroundPosition: 'center', backgroundSize: 'cover' }">
    <v-content>
      <v-row justify="end">
        <v-col md="5" class="text-end">
          <span v-if="metamaskAddress">
            <span
              :class="[ethNetwork != 'mainnet' ? 'red--text' : 'green--text']"
              >{{ ethNetwork }}
            </span>
            <span v-if="gasPrice" class="gprice mr-2"
              >(Gas Price: {{ gasPrice }})
            </span>
            <br />
          </span>
          <v-btn
            small
            color="primary"
            class="mr-2"
            v-if="!metamaskAddress"
            @click="connectWithMetamask()"
            >Connect with Metamask</v-btn
          >
          <router-link class="mr-2" v-else to="/">{{
            metamaskAddress
          }}</router-link>
          <div v-if="!metamaskAddress" class="mt-20"></div>
        </v-col>
      </v-row>
      <div
        v-if="
          this.$route.path !== '/login' &&
          this.$route.path !== '/token'
        "
      >
        <h3 class="mlr-15">Making this big world small just for you!</h3>

        <div v-if="this.$route.path !== '/stake'" class="index-banner">
          <img :src="bannerValue" alt="" style="width: 100%; cursor: pointer;" class="mt-3" @click="goHome()" />
        </div>

        <div id="nav">
          <span v-if="logged">
            <router-link class="fadmin" to="/admin">Admin</router-link>
          </span>

        <router-view v-if="this.$route.path !== '/'" />

        <v-row>
          <v-col cols="12" xl="3" lg="4" md="4" xs="12" sm="12" v-for="city in cities" :key="toSlug(city.name)">
            <router-link
              class="fcity"
              :to="{ name: 'City', params: { city: toSlug(city.name) } }"
              >{{ city.name }}</router-link>
              <v-img :src="city.img" max-height="200px" contain></v-img>
          </v-col>
        </v-row>

        <router-view v-if="this.$route.path === '/'" />

          <router-link class="fcity" to="/about">About</router-link>
        </div>
      </div>
      <router-view v-if="this.$route.path === '/login'" />
      <TxTable />
      <div class="pb-x12"></div>
      
      <v-row>
        <v-col>
          <span>
            <img
              class="dif mr-2"
              width="50"
              alt="XYR"
              src="./assets/left.png"
            />
            <h1 class="dif">
              <span class="cpoint" @click="goHome()">ALLY FOCUS</span>
            </h1>
            <img class="dif" width="50" alt="XYR" src="./assets/right.png" />
          </span>
        </v-col>
      </v-row>

      <v-row>
        <v-col>
          <img alt="XYR" src="./assets/ft.png" />
        </v-col>
      </v-row>
    </v-content>
  </v-app>
</template>
<script>
import TxTable from "@/components/table/TxTable.vue";
var Web3 = require("web3");
import backgroundUrl from "@/assets/bg.png";

export default {
  components: {
    TxTable,
  },
  data() {
    return {
      bannerValue: "",
      backgroundUrl,
      userAddreses: [],
      metamaskAddressList: [],
      connector: null,
    };
  },
  watch: {
    metamaskAddress(newValue) {
      if (window.tidioChatApi) {
        window.tidioChatApi.addVisitorTags([newValue]);
      } else {
        if (!this.metamaskAddressList.includes(newValue))
          this.metamaskAddressList.push(newValue);
      }
    },
  },
  computed: {
    metamaskAddress() {
      return this.$store.state.metamaskAddress;
    },
    gasPrice() {
      return Number(this.$store.state.gasPrice).toFixed();
    },
    ethNetwork() {
      const network = this.$store.state.ethNetwork;
      return network == 1 ? "mainnet" : "testnet";
    },
    logged() {
      return this.$store.state.profile.uid || this.$cookie.get("uid");
    },
    cities() {
      return this.$store.getters.cities;
    },
  },
  methods: {
    goCity(city) {
      this.$router.push("/" + city);
    },
    openStakeApp() {
      this.$router.push("/stake");
    },
    connectWithMetamask() {
      if (window.ethereum) {
        window.web3 = new Web3(window.ethereum);
        window.ethereum.send("eth_requestAccounts");
        this.$store.commit(
          "setMetamaskAddress",
          window.ethereum.selectedAddress
        );
        var _this = this;
        window.ethereum.on("accountsChanged", async (accounts) => {
          _this.$store.commit("setMetamaskAddress", accounts[0]);
        });
        window.ethereum.on("networkChanged", async (networkId) => {
          _this.$store.commit("setEthNetwork", networkId);
        });
        this.$store.commit("setEthNetwork", window.ethereum.networkVersion);
        return true;
      }
      return false;
    },
    toSlug(text) {
      return text.trim().toLowerCase().replace(" ", "");
    },
    goHome() {
      if (this.$route.path != "/") {
        this.$router.push("/");
      }
    },
    compare(a, b) {
      if (b.key > a.key) return -1;
      if (b.key < a.key) return 1;
      return 0;
    },
    loadBanner() {
      this.$http
        .get(this.$HOST + "/api/get/static/banner", { withCredentials: true })
        .then((resp) => {
          this.bannerValue = resp.data.val;
        });
    },
    getCities() {
      var cities = [];
      this.$http
        .get(this.$HOST + "/api/search/cities", { withCredentials: true })
        .then((resp) => {
          resp.data.sort(this.compare);
          resp.data.forEach((doc) => {
            cities.push({
              name: doc._id,
              img: doc.img,
            });
          });
        });
      this.$store.commit("setCities", cities);
    },
    getCategories() {
      var categories = [];
      this.$http
        .get(this.$HOST + "/api/search/categories", { withCredentials: true })
        .then((resp) => {
          resp.data.forEach((doc) => {
            categories.push({
              name: doc._id,
            });
          });
        });
      this.$store.commit("setCategories", categories);
    },
    onTidioChatApiReady() {
      window.tidioChatApi.addVisitorTags(this.metamaskAddressList);
    },
  },
  created() {
    this.loadBanner();
  },
  mounted() {
    this.connectWithMetamask();
    this.getCities();
    this.getCategories();
    if (this.$cookie.get("uid")) {
      this.$store.commit("setProfile", { uid: this.$cookie.get("uid") });
    }
    var _this = this;
    if (window.tidioChatApi) {
      window.tidioChatApi.on("ready", _this.onTidioChatApiReady);
    } else {
      document.addEventListener("tidioChat-ready", _this.onTidioChatApiReady);
    }
  },
};
</script>
<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-size: cover;
  /* color: #ffffff99; */
}

.gprice {
  font-size: 0.9em;
}

.fadmin {
  font-size: 2em;
  font-weight: bold;
  color: #ff5d5d !important;
}

.fcity {
  font-size: 2em;
  font-weight: bold;
  color: #1876d2 !important;
}
#nav a.router-link-exact-active {
  color: #42b983 !important;
}

.fwb {
  font-weight: bold;
  font-size: 2em;
}

#nav {
  padding: 30px;
}

.dif {
  display: inline-flex;
}

#nav a {
  font-weight: bold;
  /* color: #ffffff99; */
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.mlr-15 {
  margin-left: 15px;
  margin-right: 15px;
}

.mt-20 {
  margin-top: 20px;
}

.tdn {
  text-decoration: none !important;
  color: #2c3e50 !important;
}

.tdn-t {
  text-decoration: none !important;
}

.cpoint {
  cursor: pointer;
}

.pb-x12 {
  padding-bottom: 600px;
}
.pb-40 {
  padding-bottom: 40px;
}

.index-banner {
  position: relative;
}

.index-banner__btn {
  position: absolute !important;
  top: 42px;
  right: 30px;
  z-index: 1000;
}

@media screen and (max-width: 576px) {
  .index-banner__btn {
    top: 22px;
    right: 10px;
  }
}
</style>