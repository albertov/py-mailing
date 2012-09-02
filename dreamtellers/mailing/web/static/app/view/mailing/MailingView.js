Ext.define('WebMailing.view.mailing.MailingView', {
    extend: 'Ext.panel.Panel',
    alias: 'widget.mailingview',
    html: '<iframe frameborder="0" width="100%" height="100%" />',
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
     },
     reload: function() {
         this.setSrc(this.src);
     }
});

