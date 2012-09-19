Ext.define('WebMailing.view.mailing.View', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mailing_view',
    html: '<iframe frameborder="0" width="100%" height="100%" />',
    src: null,
    listeners: {
        afterrender: function() {
            this.iframe = this.getEl().query('iframe')[0];
            if (this.src) {
                this.setSrc(this.src);
            }
        }
    },
    setSrc: function(src) {
        this.src = src;
        if (this.iframe) {
            this.iframe.src = src;
        } else {
            console.warn("Cannot setUrl because iframe hasn't been rendered");
        }
     }
});

