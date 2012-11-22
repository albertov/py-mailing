Ext.define('WebMailing.store.Templates', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Template',
    model: 'WebMailing.model.Template',
    remoteSort: true,
    buffered: true,
    autoSync: true,
    pageSize: 100,
    sorters: [{
        property: 'title',
        direction: 'ASC'
    }],
    
});
