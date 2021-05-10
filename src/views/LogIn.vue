<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Log In</v-toolbar-title>
            <v-spacer></v-spacer>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form">
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                name="email"
                required
                prepend-icon="mdi-account"
              ></v-text-field>

              <v-text-field
                v-model="password"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                label="Password"
                :rules="[passwordRules.required, passwordRules.min]"
                hint="At least 8 characters"
                prepend-icon="mdi-lock"
                counter
                @click:append="showPassword = !showPassword"
              ></v-text-field>
            </v-form>
            <span class="red--text" v-text="responseError"></span>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn :loading="loading" color="primary" @click="login">Log In</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      emailRules: [
        v => !!v || "E-mail is required",
        v => /.+@.+\..+/.test(v) || "E-mail must be valid"
      ],
      password: "",
      passwordRules: {
        required: value => !!value || "Password is required.",
        min: v => v.length >= 8 || "Min 8 characters"
      },
      showPassword: false,
      loading: false,
      responseError: '',
    };
  },
  methods: {
    login() {
      if (this.$refs.form.validate()) {
        this.loading = true;
        this.responseError = '';
        this.$firebase.auth().signInWithEmailAndPassword(this.email, this.password)
        .then(response => {
            this.loading = false;
            this.$cookie.set('uid', response.user.uid);
            this.$store.dispatch('setProfile', {uid: response.user.uid})
            this.$router.push("/");
          })
          .catch(error => {
            this.loading = false;
            this.responseError = error.message;
          });
      }
    }
  },
  computed: {
    emailErrors() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      !this.$v.email.email && errors.push("Must be valid e-mail");
      !this.$v.email.required && errors.push("E-mail is required");
      return errors;
    },
  }
};
</script>