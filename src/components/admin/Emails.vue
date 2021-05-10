<template>
  <v-container fluid>
    <v-sheet elevation="12" class="pa-5 mt-4">
      <v-textarea
        v-model="emailsCSV"
        label="Emails"
        :no-resize="false"
        outlined
        placeholder="date,email,address,campaign,uid"
        :row-height="16"
        :rows="20"
        readonly
      ></v-textarea>
    </v-sheet>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    emailsCSV: "",
  }),
  watch: {
    activeTab(num) {
      if (num == 6) {
        this.loadEmails();
      }
    }
  },
  methods: {
    loadEmails() {
      this.$http
        .get(
          this.$HOST + "/api/db/emails" + "?uid=" + this.$cookie.get("uid"),
          {
            withCredentials: true,
          }
        )
        .then((resp) => {
          this.emailsCSV = "date,email,address,campaign,uid\n";
          this.emailsCSV += resp.data;
        });
    },
  },
  mounted() {
    this.loadEmails();
  },
};
</script>