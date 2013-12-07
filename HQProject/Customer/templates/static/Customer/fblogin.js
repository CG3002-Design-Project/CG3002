
FB.login(function(response) (
    if (response.session) {
        if (response.perms) {
            /* user is logged in and
               granted some permissions. */
            /* perms is a comma separated
               list of granted permissions */
        } else {
            /* user is logged in, but did
               not grant any permissions */
        } else {
            /* user is not logged in */
        }
}, {perms:'read_stream,
           publish_stream,
           offline_access'});