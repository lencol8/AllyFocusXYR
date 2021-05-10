<template>
  <div class="token">
    <v-row justify="center">
      <v-col class="t-form elevation-5">
        <!-- <h1>XYR</h1> -->
        <div class="pt-5">
          <v-btn depressed x-large :color="tabColor(1)" @click="selectTab(1)">CLAIM</v-btn>
          <v-btn depressed x-large :color="tabColor(2)" @click="selectTab(2)" class="ml-15 mr-15">SEND</v-btn>
          <v-btn depressed x-large :color="tabColor(3)" @click="selectTab(3)">ETH/XYR</v-btn>
          <br>
          <!-- <div class="mt-3"></div> -->
          <!-- <v-btn depressed x-large :color="tabColor(4)" @click="selectTab(4)">ETH/USDT</v-btn>
          <v-btn depressed x-large :color="tabColor(5)" @click="selectTab(5)" class="ml-15 mr-15">USDT/ETH</v-btn>
          <v-btn depressed x-large :color="tabColor(6)" @click="selectTab(6)">USDT/XYR</v-btn> -->
        </div>
        <div class="mt-30" v-if="currentTab == 1">
          <img @click="increaseTap" alt="XYR" src="../assets/xyr.png" />
          <h2 class="mt-30">
            ALLYFOCUS Faucet<br>Claim free XYR tokens here
          </h2>
          <v-btn @click="claim()" x-large class="mt-30" depressed color="error">Claim 5 XYR</v-btn>
        </div>
        <div v-if="currentTab == 2">
          <h4 class="mt-15">XYR Balance: {{ xyrBalance }}</h4>
          <v-text-field v-model="recipient" label="Recipient address" dense outlined class="pt-10"></v-text-field>
          <v-text-field v-model="recipientAmount" type="number" label="XYR" dense outlined></v-text-field>
          <v-btn x-large class="mt-15" depressed color="error" @click="send()">Send</v-btn>
        </div>
        <div class="mt-30" v-if="currentTab == 3">
          <h2>Exchange Rate</h2>
          <p>
            1 XYR = {{exchangeRateETH}} ETH
            <br />
            1 XYR = {{exchangeRateUSD}} USD
          </p>
          <v-text-field v-model="buyAmount" type="number" label="ETH Amount" dense outlined></v-text-field>
          <v-btn x-large depressed color="error" @click="buy()">Buy</v-btn>
          <h2 class="mt-15">OR</h2>
          <p class="mt-30">
            Send ETH to this address in order
            <br />to receive XYR
          </p>
          <p>{{ tokenAddress }}</p>
          <!-- <img alt="XYR" src="../assets/qr.png"> -->
          <qrcode-vue v-if="tokenAddress" class="img" :value="'ethereum:' + tokenAddress + '?amount=' + buyAmount" level="H" :size="154"></qrcode-vue>
        </div>
        <!-- *** ETH/USDT *** -->
        <div class="mt-30" v-if="currentTab == 4">
          <h2>Exchange Rate</h2>
          <p>
            1 ETH = {{exchangeRateETHUSDT}} USDT
          </p>
          <p>
            ETH Balance: {{ metamaskBalance }}
          </p>
          <v-row justify="center">
            <v-col md="6" class="pb-0">
              <v-text-field v-model="swapUSDTETHAmountETH" type="number" label="Send ETH" dense outlined></v-text-field>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col md="6">
              <v-text-field v-model="swapUSDTETHAmountUSD" type="number" label="Recieve USDT" dense outlined></v-text-field>
            </v-col>
          </v-row>
          <v-btn :disabled="!ethUsdtSwapEnabled" x-large depressed color="error" @click="swapETHForExactTokens()">Swap</v-btn>
        </div>
        <!-- *** USDT/ETH *** -->
        <div class="mt-30" v-if="currentTab == 5">
          <h2>Exchange Rate</h2>
          <p>
            1 USDT = {{exchangeRateUSDTETH}} ETH
          </p>
          <p>
            USDT Balance: {{ usdtBalance }}
          </p>
          <v-row justify="center">
            <v-col md="6" class="pb-0">
              <v-text-field v-model="swapUSDTETHAmountUSD" type="number" label="Send USDT" dense outlined></v-text-field>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col md="6">
              <v-text-field v-model="swapUSDTETHAmountETH" type="number" label="Receive ETH" dense outlined></v-text-field>
            </v-col>
          </v-row>
          <v-btn v-if="!usdtEthSwapEnabled" x-large depressed color="cyan accent-4" class="mr-1 white--text" @click="approveUSDTForUniswap()">Approve USDT For Swap</v-btn>
          <v-btn v-if="usdtEthSwapEnabled" x-large depressed color="error" @click="swapExactTokensForETH()">Swap</v-btn>
        </div>
        <br />
        <a :href="etherscanAddress" target="_blank">AllyFocus Etherscan Transactions</a>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import QrcodeVue from "qrcode.vue";
const Web3 = require("web3");
var infura = new Web3();
import moment from "moment";

export default {
  name: "Token",
  components: {
    QrcodeVue
  },
  data() {
    return {
      currentTab: 1,
      recipient: "",
      recipientAmount: "",
      buyAmount: "",
      tapTap: 0,
      exchangeRateETHUSDT: "",
      exchangeRateUSDTETH: "",
      exchangeRateETH: "",
      exchangeRateUSD: "",
      swapUSDTETHAmountUSD: "",
      ethUsdtSwapEnabled: false,
      usdtEthSwapEnabled: false,
      usdtBalance: 0,
      xyrBalance: 0,
      metamaskBalance: 0,
      uniswapUSDTAllowance: 0,
      balancesTimer: null,
      exchangeRateTimer: null,
      maxAllowance: '115792089237316195423570985008687907853269984665640564039457584007913129639935',
    };
  },
  watch: {
    metamaskAddress() {
      this.updateBalances()
    },
    swapUSDTETHAmountUSD(newValue) {
      if (this.swapUSDTETHAmountUSD > 0 && this.uniswapUSDTAllowance >= this.swapUSDTETHAmountUSD
          || this.uniswapUSDTAllowance == this.maxAllowance) {
        this.usdtEthSwapEnabled = true
      } else {
        this.usdtEthSwapEnabled = false
      }
      newValue > 0 ? this.ethUsdtSwapEnabled = true : this.ethUsdtSwapEnabled = false;
    },
    uniswapUSDTAllowance(newValue) {
      if (newValue > 0 && this.swapUSDTETHAmountUSD < newValue
          || (!this.swapUSDTETHAmountUSD && newValue > 0)
          || this.uniswapUSDTAllowance == this.maxAllowance) {
        this.usdtEthSwapEnabled = true
      } else {
        this.usdtEthSwapEnabled = false
      }
    }
  },
  computed: {
    swapUSDTETHAmountETH: {
       get: function() {
          return this.swapUSDTETHAmountUSD ? Number(this.swapUSDTETHAmountUSD / this.exchangeRateETHUSDT).toFixed(8) : '';
       },
       set: function(newValue) {
         newValue > 0 ? Number(this.swapUSDTETHAmountUSD = newValue * this.exchangeRateETHUSDT).toFixed(6) : this.swapUSDTETHAmountUSD = '';
       }
    },
    etherscanAddress() {
      return "https://etherscan.io/address/" + this.tokenAddress;
    },
    metamaskAddress() {
      return this.$store.state.metamaskAddress;
    },
    gasPrice() {
      return window.web3.utils.toWei(this.$store.state.gasPrice, "gwei");
    },
    contractABI() {
      return this.$store.state.contractABI;
    },
    uniswapABI() {
      return this.$store.state.uniswapABI;
    },
    usdtABI() {
      return this.$store.state.usdtABI;
    },
    WETHAddress() {
      return this.$store.state.WETHAddress;
    },
    USDTAddress() {
      return this.$store.state.USDTAddress;
    },
    uniswapAddress() {
      return this.$store.state.uniswapAddress;
    },
    tokenAddress() {
      return this.$store.state.tokenAddress;
    },
    infuraURL() {
      return this.$store.state.infuraURL;
    },
    ehtApiKey() {
      return this.$store.state.etherscanApiKeys[2];
    },
    connector() {
      return this.$store.state.connector;
    },
  },
  methods: {
    async updateBalances() {
      if (this.metamaskAddress) {
        this.getUniswapUSDTAllowance()
        this.getUSDTBalance()
        this.getMetamaskBalance()
        this.getXYRBalance()
        this.getGasPrice()
      }
    },
    async getUniswapUSDTAllowance() {
      let contract = new window.web3.eth.Contract(
        this.usdtABI,
        this.USDTAddress
      );
      this.uniswapUSDTAllowance = await contract.methods.allowance(this.metamaskAddress, this.uniswapAddress).call();
    },
    async getUSDTBalance() {
      let contract = new window.web3.eth.Contract(
        this.usdtABI,
        this.USDTAddress
      );
      let usdtBalance = await contract.methods.balanceOf(this.metamaskAddress).call();
      this.usdtBalance = Number(window.web3.utils.fromWei(usdtBalance, 'mwei')).toFixed(6);
    },
    async getXYRBalance() {
      let contract = new window.web3.eth.Contract(
        this.contractABI,
        this.tokenAddress
      );
      let xyrBalance = await contract.methods.balanceOf(this.metamaskAddress).call();
      this.xyrBalance = Number(window.web3.utils.fromWei(xyrBalance, 'ether')).toFixed(6);
    },
    async approveUSDTForUniswap() {
      let contract = new window.web3.eth.Contract(
        this.usdtABI,
        this.USDTAddress,
        { from: this.metamaskAddress }
      );
      let maxUINT = '0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'; // max uint 2 ** 256
      await contract.methods.approve(this.uniswapAddress, maxUINT).send({ gasPrice: this.gasPrice.toString() });
    },
    async swapExactTokensForETH() {
      if (this.usdtBalance > 0 && this.swapUSDTETHAmountUSD > 0) {
        let contract = new window.web3.eth.Contract(
          this.uniswapABI,
          this.uniswapAddress,
          { from: this.metamaskAddress }
        );
        await contract.methods.swapExactTokensForETH(
          window.web3.utils.toWei(this.swapUSDTETHAmountUSD.toString()), // amountIn
          window.web3.utils.toWei(Number(this.swapUSDTETHAmountETH * 0.995).toFixed(8).toString()), // amountOutMin | 0.5% slippage
          [this.USDTAddress, this.WETHAddress], // path [] USDT -> WETH
          this.metamaskAddress, // ETH recipient
          Number(moment.utc().format('X')) + 20, // deadline + 20 min from now
        ).send({ gasPrice: this.gasPrice.toString(), gas: '170000' });
      }
    },
    async swapETHForExactTokens() {
      if (this.swapUSDTETHAmountUSD > 0) {
        let contract = new window.web3.eth.Contract(
          this.uniswapABI,
          this.uniswapAddress,
          { from: this.metamaskAddress }
        );
        await contract.methods.swapETHForExactTokens(
          window.web3.utils.toWei(this.swapUSDTETHAmountUSD.toString(), 'mwei'),
          [this.WETHAddress, this.USDTAddress], // path [] WETH -> USDT
          this.metamaskAddress, // USDT recipient
          Number(moment.utc().format('X')) + 20, // deadline + 20 min from now
        ).send({ gasPrice: this.gasPrice.toString(), gas: '170000', value: window.web3.utils.toWei(Number(this.swapUSDTETHAmountETH).toString()) });
      }
    },
    increaseTap() {
      this.tapTap += 1;
      if (this.tapTap > 3) {
        this.tapTap = 0;
        this.$router.push("/login");
      }
    },
    selectTab(tab) {
      this.currentTab = tab;
    },
    tabColor(tab) {
      return tab == this.currentTab ? "primary" : "normal";
    },
    async buy() {
      let contract = new window.web3.eth.Contract(
        this.contractABI,
        this.tokenAddress,
        { from: this.metamaskAddress }
      );
      await contract.methods
        .buyTokens()
        .send({
          value: window.web3.utils.toWei(this.buyAmount),
          gasPrice: this.gasPrice.toString()
        });
    },
    async claim() {
      let contract = new window.web3.eth.Contract(
        this.contractABI,
        this.tokenAddress,
        { from: this.metamaskAddress }
      );
      await contract.methods.claim().send({ gasPrice: this.gasPrice.toString() });
    },
    async getExchangeRateETH() {
      let contract = new infura.eth.Contract(
        this.contractABI,
        this.tokenAddress
      );
      let resp = await contract.methods.getExchangeRate().call();
      let rate = infura.utils.fromWei(resp);
      this.exchangeRateETH = rate;
      this.getExchangeRateUSD();
    },

    async getGasPrice() {
      window.web3.eth.getGasPrice((err, gasPrice) => {
        err ? console.log(err) : this.$store.commit('setGasPrice', window.web3.utils.fromWei(gasPrice, "gwei"))
      });
    },
    async getMetamaskBalance() {
      window.web3.eth.getBalance(this.metamaskAddress, (err, balance) => {
        this.metamaskBalance = window.web3.utils.fromWei(balance, "ether")
    });

    },
    async getExchangeRateUSD() {
      this.$http
        .get(
          "https://api.etherscan.io/api?module=stats&action=ethprice&apikey=" +
            this.ehtApiKey
        )
        .then(response => {
          if (response.data.status == "1") {
            this.exchangeRateUSD = Number(parseFloat(response.data.result.ethusd) * this.exchangeRateETH).toFixed(8);
            this.exchangeRateETHUSDT = parseFloat(response.data.result.ethusd);
            this.exchangeRateUSDTETH = Number(1 / parseFloat(response.data.result.ethusd)).toFixed(8);
          } else {
            console.log(response);
          }
        })
        .catch(error => {
          window.console.log(error);
        });
    },
    async send() {
      let contract = new window.web3.eth.Contract(
        this.contractABI,
        this.tokenAddress,
        { from: this.metamaskAddress }
      );
      let v = await contract.methods
        .transfer(this.recipient, window.web3.utils.toWei(this.recipientAmount))
        .send({ gasPrice: this.gasPrice.toString() });
      console.log(v);
    }
  },
  mounted() {
    infura = new Web3(this.infuraURL);
    this.getExchangeRateETH();
    this.balancesTimer = setInterval(this.updateBalances, 5000);
    this.exchangeRateTimer = setInterval(this.getExchangeRateETH, 5000);
  },
  beforeDestroy() {
    if (this.balancesTimer) clearInterval(this.balancesTimer)
    if (this.exchangeRateTimer) clearInterval(this.exchangeRateTimer)
  },
};
</script>

<style scoped>
img {
  max-width: 150px;
}
.mt-30 {
  margin-top: 30px;
}
.mt-15 {
  margin-top: 15px;
}
.t-form {
  max-width: 500px;
  background-color: #fff;
  border-color: #fff;
  border-radius: 20px;
  margin-top: 15px;
  /* background-color: #4267B2; */
}
.mr-15 {
  margin-right: 15px;
}
.ml-15 {
  margin-left: 15px;
}
</style>