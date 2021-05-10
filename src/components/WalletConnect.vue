<template>
  <div class="wallet_connect">
    <h1>WalletConnect</h1>
  </div>
</template>

<script>
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "@walletconnect/qrcode-modal";

export default {
  name: "WalletConnect",
  data() {
    return {
      connector: null,
    };
  },
  methods: {},
  mounted() {
    console.log("mounted wc");
    this.connector = new WalletConnect({
      bridge: "https://bridge.walletconnect.org", // Required
      qrcodeModal: QRCodeModal,
    });
    if (!this.connector.connected) {
      console.log("WalletConnect create new session");
      this.connector.createSession();
    }
    this.connector.on("connect", (error, payload) => {
      if (error) {
        console.log("WalletConnect error");
        console.log(error);
      } else {
        console.log("WalletConnect payload");
        console.log(payload);
      }

      // Get provided accounts and chainId
      const { accounts, chainId } = payload.params[0];
      if (chainId == 1) {
          this.$store.commit('setMetamaskAddress', accounts[0])
          console.log('WC hook')
      }
      console.log("WalletConnect params");
      console.log(accounts);
      console.log(chainId);
    });
    this.connector.on("disconnect", (error) => {
      if (error) {
        throw error;
      }
      console.log('disconnect')
      this.$store.commit('setMetamaskAddress', '')
    });
  },
};
</script>