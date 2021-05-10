<template>
  <div class="CategoryTable">
    <v-container>
      <v-row justify="center">
        <v-col cols="12">
          <v-data-table
            :headers="headers"
            :items="categories"
            sort-by="name"
            :items-per-page="5"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat color="white">
                <v-toolbar-title>Category</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-dialog v-model="dialog" max-width="500px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn small color="orange darken-3" dark class="mb-2" v-bind="attrs" v-on="on">add category</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-container>
                        <v-row>
                          <v-col cols="12" sm="6" md="4">
                            <v-text-field v-model="editedItem.name" label="Category"></v-text-field>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                      <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
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
      { text: "Category", value: "name", align: "start", sortable: true },
      { text: "Actions", value: "actions", align: "end", sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      name: "",
    },
    defaultItem: {
      name: "",
    },
    deletedingCategory: '',
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New" : "Edit";
    },
    categories() {
      return this.$store.state.categories;
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    }
  },

  methods: {
    deleteItem(item) {
      let adminCategory = this.categories[this.categories.indexOf(item)]["name"];
      const index = this.categories.indexOf(item);
      if (confirm("Are you sure you want to delete " + adminCategory + "?")) {
        this.deleteCategory(adminCategory);
        this.categories.splice(index, 1);
        this.$store.commit("setCategories", this.categories);
      }
      this.deletedingCategory = adminCategory;
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    addCategory(name) {
      let exists = false;
      this.categories.forEach(element => {
        if (element.name.toLowerCase() == name.toLowerCase()) {
          exists = true;
          alert(name + " already exists.");
        }
      });
      if (!exists && name.trim().toLowerCase() != 'categories' && name.trim() != '') {
        this.$http.post(this.$HOST + '/api/set/categories' + '?uid=' + this.$cookie.get('uid'), JSON.stringify({key: name}), { withCredentials: true })
        this.categories.push(this.editedItem);
        this.$store.commit("setCategories", this.categories);
      }
    },
    deleteCategory(name) {
      this.$http.post(this.$HOST + '/api/delete/categories/' + name + '?uid=' + this.$cookie.get('uid'), JSON.stringify({}), { withCredentials: true })
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.categories[this.editedIndex], this.editedItem);
      } else {
        this.addCategory(this.editedItem.name);
      }
      this.close();
    }
  }
};
</script>