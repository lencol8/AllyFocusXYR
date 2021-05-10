<template>
  <div class="ContentTable">
    <v-container>
      <v-row justify="center">
        <v-col cols="10">
          <v-data-table :headers="headers" :items="content" sort-by="title" class="elevation-1">
            <template v-slot:[`item.key`]="{ item }">
              <a
                :href="'https://gateway.ipfs.io/ipfs/' + item.key"
                target="_blank"
              >{{item.key | truncate(18, '...')}}</a>
            </template>
            <template v-slot:top>
              <v-toolbar flat color="white">
                <v-icon class="mr-2" @click="clearAdminCity">mdi-arrow-left</v-icon>
                <v-toolbar-title v-text="adminCity"></v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn :loading="loading" small color="secondary" dark class="mb-2" v-bind="attrs" v-on="on">
                      <v-icon left>mdi-plus</v-icon>hash
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col sm="6" md="6">
                            <v-text-field v-model="editedItem.title" label="Title"></v-text-field>
                          </v-col>
                          <v-col sm="6" md="6">
                            <v-select
                              :items="categories"
                              label="Category"
                              v-model="editedItem.category"
                            ></v-select>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col sm="6" md="6">
                            <v-text-field v-model="editedItem.xyr" label="xyr"></v-text-field>
                          </v-col>
                          <v-col sm="6" md="6">
                            <v-text-field v-model="editedItem.eth" label="eth"></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <v-text-field v-model="editedItem.img" label="Image"></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row v-if="editedIndex === -1">
                          <v-col cols="12" sm="12" md="12">
                            <v-text-field v-model="editedItem.key" label="Hash"></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="close()">Cancel</v-btn>
                      <v-btn color="blue darken-1" text @click="save()">Save</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
              <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
              <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-container>
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
export default {
  data: () => ({
    dialog: false,
    loading: false,
    headers: [
      { text: "Title", value: "title", align: "start", sortable: true },
      { text: "Category", value: "category", align: "start", sortable: true },
      { text: "Hash", value: "key", align: "start", sortable: false },
      { text: "XYR", value: "xyr", align: "start", sortable: true },
      { text: "ETH", value: "eth", align: "start", sortable: true },
      { text: "Created", value: "created", align: "start", sortable: true },
      { text: "Actions", value: "actions", align: "end", sortable: false }
    ],
    content: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      text: "",
      key: "",
      created: moment().format("YYYY-MM-DD HH:mm:ss"),
      category: "",
      img: "",
      xyr: "",
      eth: "",
    },
    defaultItem: {
      title: "",
      text: "",
      key: "",
      created: "",
      category: "",
      img: "",
      xyr: "",
      eth: "",
    }
  }),
  computed: {
    IPFSData() {
      return this.$store.state.IPFSData;
    },
    formTitle() {
      return this.editedIndex === -1 ? "New Content" : "Edit";
    },
    adminCity() {
      return this.$store.state.adminCity;
    },
    categories() {
      let categoryNames = [""];
      this.$store.state.categories.forEach(element => {
        categoryNames.push(element.name);
      });
      return categoryNames;
    }
  },
  filters: {
    truncate: function(text, length, suffix) {
      return text.substring(0, length) + suffix;
    }
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    IPFSData(newData) {
      this.setContent(newData);
    }
  },

  created() {
    this.getIPFSContent();
  },

  methods: {
    readIPFS(hash) {
      const savedItem = this.editedItem;
      if (hash != "") {
        this.loading = true;
        ipfs.cat(hash, (err, result) => {
          if (result) {
            let allSrc = result.match(/<img.*?src="(.*?)"/);
            savedItem.text = result
              .replace(/<\/?[^>]+(>|$)/g, "")
              .replace("&nbsp;", " ")
              .replace("&nbsp;", " ")
              .trim();
            savedItem.img = allSrc != null ? allSrc[1] : '';
            if (savedItem.text) this.setContent(savedItem);
          }
          if (err) console.log(err)
          this.loading = false;
        });
      }
    },
    getIPFSContent() {
      const city = this.adminCity
        .trim()
        .toLowerCase()
        .replace(" ", "");
      this.$http
        .get(
          this.$HOST +
            "/api/search/content?args=" +
            JSON.stringify({ city: city }),
          { withCredentials: true }
        )
        .then(resp => {
          this.content = resp.data;
        });
    },
    deleteIPFSContent(contentData) {
      if (contentData) {
        this.$http.post(
          this.$HOST +
            "/api/delete/content/" +
            contentData.key +
            "?uid=" +
            this.$cookie.get("uid"),
          JSON.stringify({}),
          { withCredentials: true }
        );
      }
    },
    setContent(newData, edited) {
      if (newData  && newData.key.trim() != '') {
        var data = {
          key: newData.key,
          city: this.adminCity
            .trim()
            .toLowerCase()
            .replace(" ", ""),
          img: newData.img,
          title: newData.title,
          text: newData.text,
          created: newData.created,
          category: newData.category,
          xyr: newData.xyr,
          eth: newData.eth
        };
        this.$http.post(
          this.$HOST + "/api/set/content" + "?uid=" + this.$cookie.get("uid"),
          JSON.stringify(data),
          { withCredentials: true }
        );
        if (!edited) this.content.push(newData);
      }
    },
    clearAdminCity() {
      this.$store.commit("setAdminCity", "");
    },
    editItem(item) {
      this.editedIndex = this.content.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      let selectedContentTitle = this.content[this.content.indexOf(item)][
        "title"
      ];
      const index = this.content.indexOf(item);
      if (
        confirm("Are you sure you want to delete " + selectedContentTitle + "?")
      ) {
        this.deleteIPFSContent(this.content[index]);
        this.content.splice(index, 1);
      }
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    async save() {
      if (this.editedIndex > -1) {
        // EDIT
        this.setContent(this.editedItem, true);
        Object.assign(this.content[this.editedIndex], this.editedItem);
      } else {
        // ADD A NEW
        var exists = false;
        this.content.forEach(element => {
          if (element.key == this.editedItem.key) {
            exists = true;
            alert(element.key + " already exists.");
          }
        });
        if (!exists) {
          this.editedItem.created = moment().format("YYYY-MM-DD HH:mm:ss");
          this.readIPFS(this.editedItem.key);
        }
      }
      this.close();
    }
  }
};
</script>