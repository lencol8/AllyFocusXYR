<template>
  <div class="about">
    <v-container>
      <div v-if="about" v-html="about"></div>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      about: "",
    };
  },
  methods: {
    loadAbout() {
      this.$http
        .get(this.$HOST + "/api/get/static/about", { withCredentials: true })
        .then((resp) => {
          this.about = resp.data.val;
        });
    },
  },
  mounted() {
    this.loadAbout();
  },
};
</script>