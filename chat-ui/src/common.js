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

/**
 * Build a query string from a parameter object.
 *
 * @param params parameters as object
 * @returns {string} query string
 */
export function buildQueryString(params) {
    return Object.keys(params).reduce((pList, k) => {
        if (Array.isArray(params[k])) {
            params[k].forEach((i) => pList.push(encodeURIComponent(k) + '=' + encodeURIComponent(i)))
        } else {
            pList.push(encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
        }
        return pList
    }, []).join('&')
}

/**
 * Return a query URL for the given route.
 *
 * Pagination will be stripped from the query, so the URL always points to page 1.
 *
 * @param route route for which to generate a query URL
 * @param query search query to add to query URL
 * @param index search index (set undefined for current, null for none)
 * @returns {string} query URL
 */
export function getQueryUrl(route, query, index = undefined) {
    const qs = Object.assign({}, route.query)
    qs.q = query
    if (index) {
        qs.index = index
    } else if (index === null) {
        delete qs.index
    }
    delete qs.p
    return route.path + '?' + buildQueryString(qs)
}

/**
 * Escape HTML entities in a text.
 *
 * @param text input text
 * @returns {string}
 */
export function escapeHTML(text) {
    let e = document.createElement('_');
    e.innerText = text;
    return e.innerHTML;
}

/**
 * Abbreviate URL to at most ``maxSegments`` path segments.
 * Must be an absolute URL. Query string and fragment identifiers will be purged.
 *
 * @param url URL string to abbreviate
 * @param maxSegments: maximum number of segments
 * @param maxLength: maximum path length in characters (full URL may be longer)
 * @param replacement: abbreviation replacement character
 */
export function abbreviateUrl(url, maxSegments = 3, maxLength = 40,
                              replacement = '\u2009\u2026\u2009') {
    url = new URL(url)
    url.search = ''
    url.hash = ''

    let segments = url.pathname.substring(1).split(/\//)
    if (segments.length <= maxSegments && url.pathname.length <= maxLength) {
        return url.href
    }
    segments = segments.slice(-maxSegments)
    let path = segments.join('/').substring(-maxLength)
    return [url.origin, replacement, path].join('/')
}

/**
 * Convert rem units to px.
 *
 * @param rem rem units as float
 * @returns {number} px value
 */
export function rem2Px(rem) {
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize)
}

/**
 * Recursively transform object keys using a map function.
 *
 * @param obj input object
 * @param mapFunc mapping function taking a string and returning another string
 * @returns converted Object with transformed keys
 */
export function mapObjKeys(obj, mapFunc) {
    if (Array.isArray(obj)) {
        return obj.map((o) => mapObjKeys(o, mapFunc))
    } else if (obj !== null && typeof obj === 'object') {
        const newObj = {}
        Object.keys(obj).forEach((k) => {
            let val = obj[k]
            if (typeof obj[k] === 'object' && !Array.isArray(obj[k])) {
                val = mapObjKeys(val, mapFunc)
            }
            newObj[mapFunc(k)] = val
        })
        return newObj
    }
    return obj
}

/**
 * Recursively convert object keys from snake_case to camelCase.
 *
 * @param obj input object
 * @returns converted Object with camelCaseKeys
 */
export function objSnake2Camel(obj) {
    return mapObjKeys(obj, (s) => s.replace(/(_[a-zA-Z])/g, (m) => m[1].toUpperCase()))
}

/**
 * Recursively convert object keys from camelCase to snake_case.
 *
 * @param obj input object
 * @returns converted Object with snake_case_keys
 */
export function objCamelToSnake(obj) {
    return mapObjKeys(obj, (c) => c.replace(/([a-z][A-Z])/g, (m) => m[0] + '_' + m[1].toLowerCase()))
}

/**
 * Request token data class.
 */
export class ApiToken {
    constructor({token, timestamp, maxAge, quota}) {
        this.token = token
        this.timestamp = timestamp
        this.maxAge = maxAge
        this.quota = quota
    }
}

/**
 * Get the current request token for API and form requests.
 *
 * @returns {ApiToken} token
 */
export function getApiToken() {
    if (!window.DATA || !window.DATA.token) {
        return null
    }
    if (!(window.DATA.token instanceof ApiToken)) {
        window.DATA.token = new ApiToken(objSnake2Camel(window.DATA.token))
    }
    return window.DATA.token
}


/**
 * Get the current request CSRF token.
 *
 * @returns {ApiToken} token
 */
export function getCsrfToken() {
    if (!window.DATA || !window.DATA.csrfToken) {
        return null
    }
    return window.DATA.csrfToken
}
