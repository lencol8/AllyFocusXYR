<template>
  <div>
    <v-btn color="primary" @click="changeAddBtnState">{{ btnText }}</v-btn>
    <v-btn
      class="ml"
      v-if="showEditor"
      color="secondary"
      :loading="ipfsPushing"
      @click="addToIPFS"
    >Add to IPFS</v-btn>
    <div v-if="html_content" v-html="html_content"></div>
    <tinymce id="tinyEditor" v-if="showEditor" v-model="content" :other_options="options"></tinymce>
    <div class="pb-200"></div>
  </div>
</template>

<script>
import moment from "moment";
const IPFS = require("ipfs-mini");
const ipfs = new IPFS({
  host: "ipfs.infura.io",
  port: 5001,
  protocol: "https"
});
import tinymce from "vue-tinymce-editor";
export default {
  name: "ContentEditor",
  components: {
    tinymce: tinymce
  },
  data() {
    return {
      btnText: "Create content",
      content: "",
      html_content: "",
      showEditor: false,
      lastDocumentHash: "",
      ipfsPushing: false,
      options: {
        paste_data_images: true,
        height: 500
      }
    };
  },
  methods: {
    addToIPFS() {
      if (this.content != "") {
        this.ipfsPushing = true;
        ipfs.add(this.content, (err, result) => {
          if (result) {
            const cleanText = this.content
                .replace(/<\/?[^>]+(>|$)/g, "")
                .replace("&nbsp;", " ")
                .replace("&nbsp;", " ")
                .trim();
            const title = cleanText.slice(0, 35);
            this.lastDocumentHash = result;
            let allSrc = this.content.match(/<img.*?src="(.*?)"/);
            let img = allSrc != null ? allSrc[1] : '';
            this.$store.dispatch("setIPFSData", {
              title: title,
              text: cleanText,
              key: result,
              category: "",
              img: img,
              xyr: "",
              eth: "",
              created: moment().format("YYYY-MM-DD HH:mm:ss"),
            });
          }
          if (err) console.log(err);
          this.ipfsPushing = false;
        });
      }
    },
    readIPFS() {
      if (this.lastDocumentHash != "") {
        ipfs.cat(this.lastDocumentHash, (err, result) => {
          if (result) this.html_content = result;
          console.log(err, result);
        });
      }
    },
    changeAddBtnState() {
      this.showEditor = !this.showEditor;
      this.showEditor == true
        ? (this.btnText = "Close editor")
        : (this.btnText = "Create content");
      if (this.showEditor) this.content = "";
    }
  },
  props: {
    city: String
  }
};
</script>
<style scoped>
.ml {
  margin-left: 5px;
}
.pb-200 {
  padding-bottom: 200px;
}
</style>