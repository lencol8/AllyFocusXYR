<template>
  <div class="contentbox">
    <v-container class="pt-0">
      <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line></v-text-field>
      <v-row justify="center">
        <v-col cols="12" class="pt-0">
          <v-row v-if="content.length > 0">
            <v-col v-for="cat in categories" md="4" sm="12" :key="cat.name">
              <router-link
                class="c-link"
                :to="{ name: 'Category', params: { city: city, category: cat.name } }"
              >
                <h2 class="category">{{cat.name}}</h2>
              </router-link>

              <span v-for="item in myCategory(cat.name)" :key="item.key" class="item pl-2">
                <router-link
                  :to="{ name: 'Post', params: { city: city, category: cat.name, key: item.key } }"
                >{{item.title}}</router-link>
                <v-img :src="item.img" max-height="200px" contain></v-img>
                <v-divider></v-divider>
                <div></div>
              </span>
            </v-col>
          </v-row>
          <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      city: "",
      loading: false,
      htmlContent: null,
      content: [],
      search: "",
      searchTimer: null
    };
  },
  watch: {
    $route() {
      this.city = this.$route.params.city;
      this.getContent(this.city);
    },
    search(newValue) {
      const city = this.$route.params.city;
      if (this.searchTimer) {
        clearTimeout(this.searchTimer);
      }
      this.searchTimer = setTimeout(this.getContent, 350, city, newValue);
    }
  },
  computed: {
    categories() {
      return this.$store.state.categories;
    }
  },
  methods: {
    myCategory(name) {
      let items = [];
      this.content.forEach(element => {
        if (element.category == name) items.push(element);
      });
      return items;
    },
    clearContent() {
      this.htmlContent = null;
      this.content = [];
    },
    getContent(city, search) {
      search = search != null ? search : "";
      this.clearContent();
      if (city != "") {
        this.loading = true;
        this.$http
          .get(
            this.$HOST +
              "/api/search/content?args=" +
              JSON.stringify({ city: city }) +
              "&search=" +
              search,
            { withCredentials: true }
          )
          .then(resp => {
            this.content = resp.data;
            this.loading = false;
          })
          .catch(error => {
            console.log(error);
            this.loading = false;
          });
      }
    }
  },
  mounted() {
    this.city = this.$route.params.city;
    this.getContent(this.city);
  }
};
</script>

<style>
.category {
  background-color: rgba(245, 245, 245, 0.89);
}
.c-link {
  text-decoration: none !important;
}
.bgg {
  background-color: grey;
}
.item {
  color: #1976d2;
  cursor: pointer;
  font-size: 1.17em;
  font-weight: bold;
  /* background-color: rgba(245, 245, 245, 0.89); */
}
</style>