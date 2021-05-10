<template>
    <div class="div">
        <div v-if="this.$route.path !== '/login' && this.$route.path !== '/about' && this.$route.path !== '/token'">
        <span v-if="this.$route.path !== '/admin'"><Token/></span>
        <div v-if="this.$route.path == '/'" v-html="videoValue" class="videoWrap mt-10">
        </div>
      </div>
    </div>
</template>
<script>

import Token from '@/components/Token.vue'

export default {
  components: {
    Token,
  },
  data() {
    return {
      videoValue: '',
    }
  },
  methods: {
    loadVideo() {
      this.$http.get(this.$HOST + '/api/get/static/video', { withCredentials: true }).then(resp => {
        this.videoValue = resp.data.val;
      })
    },
  },
  created() {
    this.loadVideo();
  },
}
</script>
<style lang="scss">
video {
  width: 100% !important;
  height: auto !important;
}

.videoWrap {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 */
}
.videoWrap iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

#nav {
  padding: 30px;
}

.dif {
  display: inline-flex;
}

#nav a {
  font-weight: bold;
  /* color: #ffffff99; */
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>