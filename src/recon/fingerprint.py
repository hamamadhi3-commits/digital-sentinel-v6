def fingerprint(tech_output):

    tech_output = tech_output.lower()

    detect = []

    if "wordpress" in tech_output:
        detect.append("WordPress CMS")

    if "drupal" in tech_output:
        detect.append("Drupal CMS")

    if "laravel" in tech_output:
        detect.append("Laravel PHP")

    if "django" in tech_output:
        detect.append("Django Python")

    if "react" in tech_output:
        detect.append("ReactJS")

    if "vue" in tech_output:
        detect.append("VueJS")

    if "angular" in tech_output:
        detect.append("AngularJS")

    if "cloudflare" in tech_output:
        detect.append("Cloudflare WAF")

    if "akamai" in tech_output:
        detect.append("Akamai WAF/CDN")

    return detect
