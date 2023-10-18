/*
 * Copyright 2021 Janek Bevendorff
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { createApp } from 'vue'
import InlineSvg from 'vue-inline-svg'
import ChatNoirApp from '@/ChatNoir.vue'
import router from '@/routes'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import '@/assets/css/index.css'
import {aliases} from "vuetify/iconsets/fa";
import {mdi} from "vuetify/iconsets/mdi";
import '@mdi/font/css/materialdesignicons.css';



const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const app = createApp(ChatNoirApp)
    .use(router)
    .use(vuetify)

// Fix global components not being recognized by JetBrains IDEs.
// See: https://youtrack.jetbrains.com/issue/WEB-48239
const Vue = app
Vue.component('InlineSvg', InlineSvg).mount('#app')
Vue.config.devtools = true

export default Vue
