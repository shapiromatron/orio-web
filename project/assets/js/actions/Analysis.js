import _ from 'underscore';
import * as types from '../constants/ActionTypes';
import h from '../utils/helpers';


function requestContent() {
    return {
        type: types.AN_REQUEST,
    };
}

function receiveObjects(json) {
    return {
        type: types.AN_RECEIVE_OBJECTS,
        items: json,
    };
}

function receiveObject(item){
    return {
        type: types.AN_RECIEVE_OBJECT,
        item,
    };
}

function removeObject(id){
    return {
        type: types.AN_DELETE_OBJECT,
        id,
    };
}

function fetchObject(id){
    return (dispatch, getState) => {
        let state = getState();
        if (state.analysis.isFetching) return;
        dispatch(requestContent());
        return fetch(`${state.config.analysis}${id}/`, h.fetchGet)
            .then(response => response.json())
            .then(json => dispatch(receiveObject(json)))
            .catch((ex) => console.error('Analysis parsing failed', ex));
    };
}

function setEdititableObject(object){
    return {
        type: types.AN_CREATE_EDIT_OBJECT,
        object,
    };
}

function receiveEditErrors(errors){
    return {
        type: types.AN_RECEIVE_EDIT_ERRORS,
        errors,
    };
}

function resetEditObject(){
    return {
        type: types.AN_RESET_EDIT_OBJECT,
    };
}

export function fetchObjectsIfNeeded() {
    return (dispatch, getState) => {
        let state = getState();
        if (state.analysis.isFetching) return;
        dispatch(requestContent());
        return fetch(state.config.analysis, h.fetchGet)
            .then(response => response.json())
            .then(json => dispatch(receiveObjects(json)))
            .catch((ex) => console.error('Analysis parsing failed', ex));
    };
}

export function patchObject(id, patch, cb){
    cb = cb || h.noop;
    return (dispatch, getState) => {
        let state = getState(),
            opts = h.fetchPost(state.config.csrf, patch, 'PATCH');
        return fetch(`${state.config.analysis}${id}/`, opts)
            .then(function(response){
                if (response.status === 200){
                    response.json()
                        .then((json) => dispatch(fetchObject(json.id)))
                        .then(cb())
                        .then(() => dispatch(resetEditObject()));
                } else {
                    response.json()
                        .then((json) => dispatch(receiveEditErrors(json)));
                }
            })
            .catch((ex) => console.error('Analysis parsing failed', ex));
    };
}

export function postObject(post, cb){
    cb = cb || h.noop;
    return (dispatch, getState) => {
        let state = getState(),
            opts = h.fetchPost(state.config.csrf, post);
        return fetch(state.config.analysis, opts)
            .then(function(response){
                if (response.status === 201){
                    response.json()
                        .then((json) => dispatch(receiveObject(json)))
                        .then(cb())
                        .then(() => dispatch(resetEditObject()));
                } else {
                    response.json()
                        .then((json) => dispatch(receiveEditErrors(json)));
                }
            })
            .catch((ex) => console.error('Analysis parsing failed', ex));
    };
}

export function deleteObject(id, cb){
    cb = cb || h.noop;
    return (dispatch, getState) => {
        let state = getState(),
            opts = h.fetchDelete(state.config.csrf);
        return fetch(`${state.config.analysis}${id}/`, opts)
            .then(function(response){
                if (response.status === 204){
                    dispatch(removeObject(id));
                    cb(null);
                } else {
                    response.json()
                        .then((json) => cb(json));
                }
            })
            .catch((ex) => console.error('Analysis parsing failed', ex));
    };
}

export function initializeEditForm(id=null){

    return (dispatch, getState) => {
        let state = getState(),
            object;
        if (id){
            object = _.findWhere(state.analysis.items, {id});
            object = _.extend({}, object);  // shallow-copy
        } else {
            object = {
                id: null,
                name: '',
                description: '',
                public: false,
                feature_list: null,
                genome_assembly: 1,
                sort_vector: null,
            };
        }
        dispatch(setEdititableObject(object));
    };
}