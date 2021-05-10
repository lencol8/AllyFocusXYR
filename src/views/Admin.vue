<template>
  <div class="admin">
    <v-card v-if="logged">
      <v-tabs v-model="activeTab">
        <v-tab v-for="tab of tabs" :key="tab.id">
          {{tab.name}}
        </v-tab>

        <v-tab-item>
          <v-card flat>
            <span v-if="adminCity">
              <ContentTable />
            </span>
            <span v-else>
              <v-row justify="center">
                <v-col md="8" sm="12">
                  <CityTable />
                </v-col>
              </v-row>
            </span>
            <v-container v-if="adminCity" class="pt-0">
              <v-row justify="center">
                <v-col cols="10" class="pt-0">
                  <ContentEditor />
                </v-col>
              </v-row>
            </v-container>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-row justify="center">
              <v-col md="4" sm="12">
                <CategoryTable />
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-row justify="center">
              <v-col md="4" sm="12">
                <SendTokens />
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-row justify="center">
              <v-col md="4" sm="12">
                <CustomContent />
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-row justify="center">
              <v-col md="4" sm="12">
                <Promo />
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card flat>
            <v-row justify="center">
              <v-col md="8" sm="12">
                <Emails />
              </v-col>
            </v-row>
          </v-card>
        </v-tab-item>

      </v-tabs>
    </v-card>
  </div>
</template>

<script>
import ContentEditor from "@/components/admin/ContentEditor.vue";
import CityTable from "@/components/table/CityTable.vue";
import CategoryTable from "@/components/table/CategoryTable.vue";
import ContentTable from "@/components/table/ContentTable.vue";
import SendTokens from "@/components/admin/SendTokens.vue";
import Promo from "@/components/admin/Promo.vue";
import Emails from "@/components/admin/Emails.vue";
import CustomContent from "@/components/admin/CustomContent.vue";

export default {
  name: "Admin",
  components: {
    ContentEditor,
    CityTable,
    CategoryTable,
    ContentTable,
    SendTokens,
    Promo,
    Emails,
    CustomContent,
  },
  data() {
    return {
      activeTab: this.$store.state.adminActiveTab,
      tabs: [
        { id: 1, name: 'Cities' },
        { id: 2, name: 'Category' },
        { id: 3, name: 'Send Tokens' },
        { id: 4, name: 'About/Banner/Video' },
        { id: 5, name: 'Promo Pop-Up' },
        { id: 6, name: 'Emails' },
      ]
    };
  },
  methods: {
  },
  mounted() {},
  computed: {
    logged() {
      return this.$store.state.profile.uid || this.$cookie.get("uid");
    },
    adminCity() {
      return this.$store.state.adminCity;
    },
  },
};
</script>

<style scoped>
.v-tab {
  justify-content: none;
}
</style>