<template>
  <v-container fluid>
    <v-sheet elevation="12" class="pa-5 mt-4">
      <v-select
        :items="staticItems"
        label="Content"
        v-model="selectedItem"
      ></v-select>
      <v-text-field
        outlined
        dense
        v-model="value"
        type="text"
        autocomplete="off"
        :label="label"
      ></v-text-field>
      <v-btn :loading="loading" @click="post" color="primary">POST</v-btn>
    </v-sheet>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    staticItems: ["About", "Banner", "Homepage Video"],
    selectedItem: "About",
    value: "",
    label: "Text/HTML",
    loading: false,
  }),
  watch: {
    selectedItem(newVal) {
      if (newVal == "Banner") {
        this.label = "URL/Base64";
      } else if (newVal == "Homepage Video") {
        this.label = "Youtube iframe";
      } else if (newVal == "About") {
        this.label = "Text/HTML";
      }
      this.getStatic();
    },
  },
  methods: {
    getKey() {
      if (this.selectedItem == "Banner") return "banner";
      if (this.selectedItem == "Homepage Video") return "video";
      if (this.selectedItem == "About") return "about";
    },
    getStatic() {
      this.$http
        .get(this.$HOST + "/api/get/static/" + this.getKey(), {
          withCredentials: true,
        })
        .then((resp) => {
          this.value = resp.data.val;
        });
    },
    post() {
      let key = this.getKey();
      if (key) {
        this.loading = true;
        this.$http.post(
          this.$HOST + "/api/set/static" + "?uid=" + this.$cookie.get("uid"),
          JSON.stringify({ key: key, val: this.value }),
          { withCredentials: true }
        );
        this.loading = false;
      }
    },
  },
  mounted() {
    this.getStatic();
  },
};
</script>