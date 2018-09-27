// reader.js

Vue.component('book-section', {
  props: ['title', 'showing'],
  template: `
    <section href='#' v-show='showing==title'>
      <h1>{{title}}</h1>
      <slot></slot>
    </section>
  `
})

new Vue({
  el: "#book",
  data: {
    showing: 'Table of Content'
  }
})