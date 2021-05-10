<template>
  <v-container fluid>
    <v-sheet elevation="12" class="pa-5 mt-4">
      <div class>{{info}}</div>
      <v-text-field outlined dense v-model="account" type="text" autocomplete="off" label="Account"></v-text-field>
      <v-text-field outlined dense v-model="pkey" type="password" autocomplete="new-password" label="Private key"></v-text-field>
      <v-text-field outlined dense v-model="gasPrice" type="text" label="Gas price"></v-text-field>
      <v-textarea
        v-model="fieldModel"
        label="Each recipient in a new line"
        :loading="loading"
        :no-resize="noResize"
        outlined
        :placeholder="placeholder"
        :row-height="rowHeight"
        :rows="rows"
      ></v-textarea>
      <v-btn @click="sendTx" color="primary">Send</v-btn>
    </v-sheet>
  </v-container>
</template>

<script>
var EthereumTx = require("ethereumjs-tx").Transaction;
const Web3 = require("web3");
var web3 = new Web3();

export default {
  data() {
    return {
      showPkey: true,
      clearable: true,
      loading: false,
      noResize: false,
      outlined: false,
      placeholder: "address,amount",
      rowHeight: 16,
      rows: 2,
      info: "",
      fieldModel: "", //"0xfDAacc9935E7F02187986C59265270868B43A6ca,0.001",
      account: "", //"0x1920Ec7Aeb55be6b83C93B34260df3cA06557311",
      pkey: "", //"0x87f35330dc3808922198f8a828c10db903102812027f2a05283134863773a0d1",
      gasPrice: "10"
    };
  },
  computed: {
    tokenAddress() {
      return this.$store.state.tokenAddress;
    },
    contractABI() {
      return this.$store.state.contractABI;
    },
    infuraURL() {
      return this.$store.state.infuraURL;
    }
  },
  methods: {
    async getTxCount() {
      return web3.eth.getTransactionCount(this.account);
    },
    async sendTx() {
      this.loading = true;
      try {
        var txRows = this.fieldModel.split("\n");
        if (txRows.length > 0) {
          var txList = [];
          var txCount = await this.getTxCount();
          txRows.forEach(element => {
            console.log(element);
            const recipient = element.split(",")[0];
            const amount = web3.utils.toWei(element.split(",")[1]);
            let contract = new window.web3.eth.Contract(
              this.contractABI,
              this.tokenAddress,
              { from: this.metamaskAddress }
            );
            const txData = contract.methods
              .transfer(recipient, amount)
              .encodeABI();
            const txObject = {
              nonce: web3.utils.toHex(txCount),
              from: this.account,
              to: this.tokenAddress,
              gasPrice: web3.utils.toHex(
                web3.utils.toWei(this.gasPrice, "gwei")
              ),
              gasLimit: web3.utils.toHex(100000),
              data: txData
            };

            console.log(txObject);
            const privateKey = new Buffer.from(this.pkey.slice(2), "hex");
            const tx = new EthereumTx(txObject);
            tx.sign(privateKey);
            const serializedTx = tx.serialize();
            const _rawTx = "0x" + serializedTx.toString("hex");
            txList.push(_rawTx);
            txCount++;
          });
          console.log(txList);
          txList.forEach(rawTx => {
            web3.eth.sendSignedTransaction(rawTx);
          });
          this.loading = false;
        }
      } catch (error) {
        console.log(error);
        this.loading = false;
      }
    }
  },
  mounted() {
    web3 = new Web3(
      this.infuraURL
    );
  }
};
</script>