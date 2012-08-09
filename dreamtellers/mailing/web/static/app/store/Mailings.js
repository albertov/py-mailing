Ext.define('WebMailing.store.Mailings', {
    extend: 'Ext.data.Store',
    requires: 'WebMailing.model.Mailing',
    model: 'WebMailing.model.Mailing',
    remoteSort: true
});
