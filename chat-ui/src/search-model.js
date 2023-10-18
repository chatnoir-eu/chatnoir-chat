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


import { objSnake2Camel, objCamelToSnake } from '@/common'

/**
 * Index meta descriptor.
 */
export class IndexDesc {
    constructor({id, name, selected}) {
        this.id = id
        this.name = name
        this.selected = selected || false
    }
}

export class SearchResponse {
    constructor(meta, results) {
        this.meta = meta || {}
        this.results = results || []
    }
}

export class SearchModel {
    constructor({query, indices, page, pageSize} = {}) {
        this.query = query || ''
        this.pageSize =  parseInt(pageSize) || 10
        this.page = Math.max(1, parseInt(page)) || 1
        this.response = null
        this.setIndices(indices)
    }

    /**
     * Generate a query string object representation of the search model's request data.
     */
    toQueryStringObj() {
        let indices = this.selectedIndices().map((e) => e.id)
        return {
            q: this.query,
            index: indices.length === 1 ? indices[0] : indices,
            p: this.page,
        }
    }

    /**
     * Generate an API request body representation of the search model's request data.
     * @param additionalFields additional fields to add to the request body
     */
    toApiRequestBody(additionalFields = null) {
        if (!additionalFields) {
            additionalFields = {}
        }
        return objCamelToSnake({
            query: this.query,
            index: this.selectedIndices().map((e) => e.id),
            from: Math.max(0, this.page - 1) * this.pageSize,
            size: this.pageSize,
            extendedMeta: true,
            ... additionalFields
        })
    }

    /**
     * Update model from search result JSON response.
     *
     * @param jsonData JSON response data
     */
    updateFromResponse(jsonData) {
        const response = new SearchResponse(objSnake2Camel(jsonData.meta), objSnake2Camel(jsonData.results))
        response.meta.indices = response.meta.indices.map((i) => new IndexDesc(i))
        this.response = response
        
        this.page = Math.floor(this.response.meta.resultsFrom / this.response.meta.pageSize) + 1
        this.pageSize = this.response.meta.pageSize
        this.setIndices(this.response.meta.indices)
    }

    /**
     * Update request model data from a query string object and reset response.
     *
     * @param queryString query string Object
     */
    updateFromQueryString(queryString) {
        let queryIndices = queryString.index || []
        if (typeof queryIndices === 'string') {
            queryIndices = [queryIndices]
        }

        this.query = queryString.q || ''
        if (this.indices.length === 0) {
            this.setIndices()
        }
        this.indices = this.indices.map((i) => Object.assign(
            {}, i, {selected: !queryIndices.length ? i.selected : queryIndices.includes(i.id)}))
        this.page = Math.max(1, parseInt(queryString.p) || 1)
        this.response = null
    }

    /**
     * Get maximum page from search result or 0 if unavailable.
     */
    maxPage() {
        if (!this.response) {
            return 0
        }
        return this.response.meta.maxPage
    }

    /**
     * Update list of available and selected from a list of (JSON) objects with the following shape:
     * `{id: "index_id", name: "Index name", selected: true | false}`.
     *
     * If `indices` is unset, the list will be refreshed from `window.DATA.indices` if available.
     *
     * @param indices list of `IndexDesc` objects or undefined
     */
    setIndices(indices = null) {
        if (!indices) {
            this.setIndices(window.DATA.indices || [])
            return
        }
        this.indices = indices.map((i) => i instanceof IndexDesc ? i : new IndexDesc(i))
    }

    /**
     * Return the list of selected indices (i.e., `index.selected === true`).
     */
    selectedIndices() {
        return this.indices.filter((e) => e.selected)
    }
}
