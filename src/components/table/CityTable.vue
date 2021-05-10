<template>
  <div class="CityTable">
    <v-container>
      <v-row justify="center">
        <v-col cols="12">
          <v-data-table
            :headers="headers"
            :items="cities"
            sort-by="name"
            class="elevation-1"
            @click:row="selectItem"
          >
            <template v-slot:top>
              <v-toolbar flat color="white">
                <v-toolbar-title>The United States</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn small color="primary" dark class="mb-2" v-bind="attrs" v-on="on">add city</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row v-if="editedIndex === -1">
                          <v-col>
                            <v-text-field v-model="editedItem.name" label="City"></v-text-field>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <v-text-field v-model="editedItem.img" label="Image"></v-text-field>
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
              <v-icon small class="mr-2" @click.stop="editItem(item)">mdi-image-edit</v-icon>
              <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    headers: [
      { text: "City", value: "name", align: "start", sortable: true },
      { text: "Actions", value: "actions", align: "end", sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      name: "",
      url: "",
      img: "",
    },
    defaultItem: {
      name: "",
      url: "",
      img: "",
    },
    deletedingCity: '',
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New" : "Edit";
    },
    cities() {
      return this.$store.state.cities;
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    selectItem(item) {
      let adminCity = this.cities[this.cities.indexOf(item)]["name"];
      if (this.deletedingCity == '') {
        this.$store.commit("setAdminCity", adminCity);
      }
      this.deletedingCity = ''
    },
    editItem(item) {
      this.editedIndex = this.cities.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      let adminCity = this.cities[this.cities.indexOf(item)]["name"];
      const index = this.cities.indexOf(item);
      if (confirm("Are you sure you want to delete " + adminCity + "?")) {
        this.deleteCity(adminCity);
        this.cities.splice(index, 1);
        this.$store.commit("setCities", this.cities);
      }
      this.deletedingCity = adminCity;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    setCity(item, edited) {
      let exists = false;
      this.cities.forEach(element => {
        if (element.name.toLowerCase() == item.name.toLowerCase()) {
          exists = true;
          if (!edited) alert(item.name + " already exists.");
        }
      });
      if ((!exists || edited) && item.name.trim().toLowerCase() != 'cities' && item.name.trim() != '') {
        this.$http.post(this.$HOST + '/api/set/cities' + '?uid=' + this.$cookie.get('uid'), JSON.stringify({
          key: item.name, img: this.editedItem.img
        }), { withCredentials: true })
        if (!edited) {
          this.editedItem.url = this.editedItem.name.toLowerCase().replace(' ', '')
          this.cities.push(this.editedItem);
          this.$store.commit("setCities", this.cities);
        }
      }
    },
    deleteCity(name) {
      this.$http.post(this.$HOST + '/api/delete/cities/' + name + '?uid=' + this.$cookie.get('uid'), JSON.stringify({}), { withCredentials: true })
    },
    save() {
      if (this.editedIndex > -1) {
        this.setCity(this.editedItem, true);
        Object.assign(this.cities[this.editedIndex], this.editedItem);
      } else {
        this.setCity(this.editedItem);
      }
      this.close();
    }
  }
};
</script>