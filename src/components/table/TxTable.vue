<template>
  <div class="CategoryTable">
    <v-container>
      <v-tabs v-model="tab">
        <v-tab class="tdn-t" v-for="item in items" :key="item.tab">{{ item.tab }}</v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab">
        <v-tab-item v-for="item in items" :key="item.tab">
          <v-card flat>
            <v-card-text></v-card-text>
          </v-card>

          <v-data-table
            :headers="item.headers"
            :items="item.transactions"
            :items-per-page="5"
            sort-by="timeStamp"
            sort-desc
            class="elevation-1 mi-dataTable"
          >
            <template v-slot:no-data>
              <v-btn :loading="loading" text color="primary" @click="etherscanTxList(tab)">update</v-btn>
            </template>

            <template slot="footer">
              <v-btn
                :loading="loading"
                v-if="item.transactions.length > 0"
                color="primary"
                @click="etherscanTxList(tab, true)"
                text
                style="position: absolute; left: 10px; bottom: 10px;"
              >update</v-btn>
            </template>

            <template v-slot:[`item.hash`]="{ item }">
              <a
                :href="'https://etherscan.io/tx/' + item.hash"
                target="_blank"
              >{{item.hash | truncate(18, '...')}}</a>
            </template>

            <template v-slot:[`item.blockNumber`]="{ item }">
              <a
                :href="'https://etherscan.io/block/' + item.blockNumber"
                target="_blank"
              >{{item.blockNumber}}</a>
            </template>

            <template v-slot:[`item.timeStamp`]="{ item }">
              <span>{{ toElapsed(item.timeStamp) }}</span>
            </template>

            <template v-slot:[`item.from`]="{ item }">
              <span
                v-if="item.from.toLowerCase() == tokenAddress.toLowerCase()"
              >{{item.from | truncate(17, '...')}}</span>
              <a
                v-else
                :href="'https://etherscan.io/address/' + item.from"
                target="_blank"
              >{{item.from | truncate(17, '...')}}</a>
            </template>

            <template v-slot:[`item.to`]="{ item }">
              <a
                v-if="!item.tokenName"
                :href="'https://etherscan.io/address/' + item.to"
              >{{item.to | truncate(17, '...')}}</a>
              <a
                v-else
                :href="'https://etherscan.io/address/' + item.to"
                target="_blank"
              > {{item.tokenName}} ({{item.tokenSymbol}})</a>
            </template>

            <template v-slot:[`item.value`]="{ item }">
              <span v-if="item.tokenName">{{ toEther(item.value) }}</span>
              <span v-else>{{ toEther(item.value) }} Ether</span>
            </template>
          </v-data-table>
        </v-tab-item>
      </v-tabs-items>
    </v-container>
  </div>
</template>

<script>
import moment from "moment";
const Web3 = require("web3");
const web3 = new Web3();
export default {
  data: () => ({
    dialog: false,
    tab: null,
    apiKeyNum: 0,
    loading: false,
    items: [
      {
        tab: "Ether Txns",
        headers: [
          {
            text: "Parent Txn Hash",
            value: "hash",
            align: "start",
            width: "1%"
          },
          { text: "Block", value: "blockNumber", align: "start", width: "1%" },
          { text: "Age", value: "timeStamp", align: "start" },
          { text: "From", value: "from", align: "start" },
          { text: "To", value: "to", align: "start" },
          { text: "Value", value: "value", align: "start" }
        ],
        transactions: []
      },
      {
        tab: "Token Txns",
        headers: [
          { text: "Txn Hash", value: "hash", align: "start", width: "1%" },
          { text: "Block", value: "blockNumber", align: "start", width: "1%" },
          { text: "Age", value: "timeStamp", align: "start" },
          { text: "From", value: "from", align: "start" },
          { text: "To", value: "to", align: "start" },
          { text: "Token", value: "tokenName", align: ' d-none' },
          { text: "Token", value: "tokenSymbol", align: ' d-none' },
          { text: "Value", value: "value", align: "start" }
        ],
        transactions: []
      },
    ]
  }),

  computed: {
    etherscanApiKeys() {
      return this.$store.state.etherscanApiKeys;
    },
    categories() {
      return this.$store.state.categories;
    },
    tokenAddress() {
      return this.$store.state.tokenAddress;
    },
    metamaskAddress() {
      return this.$store.state.metamaskAddress;
    }
  },

  watch: {
    tab(newVal) {
      this.etherscanTxList(newVal);
    },
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    toElapsed(ts) {
      return moment(moment.unix(ts)).fromNow();
    },
    toEther(val) {
      return web3.utils.fromWei(val);
    },
    nextEtherscanApiKey() {
      if (this.etherscanApiKeys.length > 0) {
        this.apiKeyNum == this.etherscanApiKeys.length - 1
          ? (this.apiKeyNum = 0)
          : this.apiKeyNum++;
        return this.etherscanApiKeys[this.apiKeyNum];
      }
      return "";
    },
    filterMyXYR(txns) {
      var myXYRTxns = [];
      if (this.metamaskAddress) {
        txns.forEach(element => {
          if (element.tokenSymbol == 'XYR' && (element.from == this.metamaskAddress || element.to == this.metamaskAddress)) {
            myXYRTxns.push(element);
          }
        });
      }
      return myXYRTxns;
    },
    etherscanTxList(tab, force) {
      const apiKeyParam = "&apikey=" + this.nextEtherscanApiKey();
      var url =
        "https://api.etherscan.io/api?module=account&startblock=0&endblock=99999999&sort=asc&address=" +
        this.metamaskAddress +
        apiKeyParam;
      const actions = [
        "&action=txlist",
        "&action=tokentx",
      ];
      if (this.items[tab].transactions.length == 0 || force) {
        this.loading = true;
        this.$http
          .get(url + actions[tab])
          .then(response => {
            if (response.data.status == "1") {
              if (tab < 3) {
                this.items[tab].transactions = response.data.result;
              } else {
                this.items[tab].transactions = this.filterMyXYR(
                  response.data.result
                );
              }
            } else {
              console.log(response);
            }
            this.loading = false;
          })
          .catch(error => {
            window.console.log(error);
            this.loading = false;
          });
      }
    }
  },
  filters: {
    truncate: function(text, length, suffix) {
      if (text.length > 0) {
        return text.substring(0, length) + suffix;
      }
      return "";
    }
  }
};
</script>