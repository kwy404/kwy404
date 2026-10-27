#!/usr/bin/env python3
"""Builds light.svg and dark.svg, the profile banner of kwy404.

One main line with a branch for each organization that merged his pull
requests. Logos are embedded as SVG data URIs because an SVG shown through an
<img> tag cannot load external images.

Usage: python gen_banner.py [merged_pull_requests] [organizations]
"""
import base64
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MERGED_PRS = int(sys.argv[1]) if len(sys.argv) > 1 else 161
ORGS = int(sys.argv[2]) if len(sys.argv) > 2 else 54

TOP = ["Google", "Microsoft", "Meta", "Apple", "Amazon Web Services", "Mozilla", "NVIDIA", "Netflix"]
BOTTOM = ["Cloudflare", "ByteDance", "Uber", "Valve", "Adobe", "Salesforce", "Shopify", "GitHub"]

LOGOS = {
    'Google': {"bbox": [0.307, 0.0, 23.693, 24.0],
        "d": 'M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z'},
    'Microsoft': {"bbox": [0.0, 0.0, 24.0, 24.0],
        "d": 'M0 0v11.408h11.408V0zm12.594 0v11.408H24V0zM0 12.594V24h11.408V12.594zm12.594 0V24H24V12.594z'},
    'Meta': {"bbox": [0.0, 4.029, 24.0, 19.971],
        "d": 'M6.915 4.03c-1.968 0-3.683 1.28-4.871 3.113C.704 9.208 0 11.883 0 14.449c0 .706.07 1.369.21 1.973a6.624 6.624 0 0 0 .265.86 5.297 5.297 0 0 0 .371.761c.696 1.159 1.818 1.927 3.593 1.927 1.497 0 2.633-.671 3.965-2.444.76-1.012 1.144-1.626 2.663-4.32l.756-1.339.186-.325c.061.1.121.196.183.3l2.152 3.595c.724 1.21 1.665 2.556 2.47 3.314 1.046.987 1.992 1.22 3.06 1.22 1.075 0 1.876-.355 2.455-.843a3.743 3.743 0 0 0 .81-.973c.542-.939.861-2.127.861-3.745 0-2.72-.681-5.357-2.084-7.45-1.282-1.912-2.957-2.93-4.716-2.93-1.047 0-2.088.467-3.053 1.308-.652.57-1.257 1.29-1.82 2.05-.69-.875-1.335-1.547-1.958-2.056-1.182-.966-2.315-1.303-3.454-1.303zm10.16 2.053c1.147 0 2.188.758 2.992 1.999 1.132 1.748 1.647 4.195 1.647 6.4 0 1.548-.368 2.9-1.839 2.9-.58 0-1.027-.23-1.664-1.004-.496-.601-1.343-1.878-2.832-4.358l-.617-1.028a44.908 44.908 0 0 0-1.255-1.98c.07-.109.141-.224.211-.327 1.12-1.667 2.118-2.602 3.358-2.602zm-10.201.553c1.265 0 2.058.791 2.675 1.446.307.327.737.871 1.234 1.579l-1.02 1.566c-.757 1.163-1.882 3.017-2.837 4.338-1.191 1.649-1.81 1.817-2.486 1.817-.524 0-1.038-.237-1.383-.794-.263-.426-.464-1.13-.464-2.046 0-2.221.63-4.535 1.66-6.088.454-.687.964-1.226 1.533-1.533a2.264 2.264 0 0 1 1.088-.285z'},
    'Apple': {"bbox": [2.225, 0.0, 21.775, 24.0],
        "d": 'M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701'},
    'Amazon Web Services': {"bbox": [-0.0, 4.824, 24.0, 19.176],
        "d": 'M6.763 10.036c0 .296.032.535.088.71.064.176.144.368.256.576.04.063.056.127.056.183 0 .08-.048.16-.152.24l-.503.335a.383.383 0 0 1-.208.072c-.08 0-.16-.04-.239-.112a2.47 2.47 0 0 1-.287-.375 6.18 6.18 0 0 1-.248-.471c-.622.734-1.405 1.101-2.347 1.101-.67 0-1.205-.191-1.596-.574-.391-.384-.59-.894-.59-1.533 0-.678.239-1.23.726-1.644.487-.415 1.133-.623 1.955-.623.272 0 .551.024.846.064.296.04.6.104.918.176v-.583c0-.607-.127-1.03-.375-1.277-.255-.248-.686-.367-1.3-.367-.28 0-.568.031-.863.103-.295.072-.583.16-.862.272a2.287 2.287 0 0 1-.28.104.488.488 0 0 1-.127.023c-.112 0-.168-.08-.168-.247v-.391c0-.128.016-.224.056-.28a.597.597 0 0 1 .224-.167c.279-.144.614-.264 1.005-.36a4.84 4.84 0 0 1 1.246-.151c.95 0 1.644.216 2.091.647.439.43.662 1.085.662 1.963v2.586zm-3.24 1.214c.263 0 .534-.048.822-.144.287-.096.543-.271.758-.51.128-.152.224-.32.272-.512.047-.191.08-.423.08-.694v-.335a6.66 6.66 0 0 0-.735-.136 6.02 6.02 0 0 0-.75-.048c-.535 0-.926.104-1.19.32-.263.215-.39.518-.39.917 0 .375.095.655.295.846.191.2.47.296.838.296zm6.41.862c-.144 0-.24-.024-.304-.08-.064-.048-.12-.16-.168-.311L7.586 5.55a1.398 1.398 0 0 1-.072-.32c0-.128.064-.2.191-.2h.783c.151 0 .255.025.31.08.065.048.113.16.16.312l1.342 5.284 1.245-5.284c.04-.16.088-.264.151-.312a.549.549 0 0 1 .32-.08h.638c.152 0 .256.025.32.08.063.048.12.16.151.312l1.261 5.348 1.381-5.348c.048-.16.104-.264.16-.312a.52.52 0 0 1 .311-.08h.743c.127 0 .2.065.2.2 0 .04-.009.08-.017.128a1.137 1.137 0 0 1-.056.2l-1.923 6.17c-.048.16-.104.263-.168.311a.51.51 0 0 1-.303.08h-.687c-.151 0-.255-.024-.32-.08-.063-.056-.119-.16-.15-.32l-1.238-5.148-1.23 5.14c-.04.16-.087.264-.15.32-.065.056-.177.08-.32.08zm10.256.215c-.415 0-.83-.048-1.229-.143-.399-.096-.71-.2-.918-.32-.128-.071-.215-.151-.247-.223a.563.563 0 0 1-.048-.224v-.407c0-.167.064-.247.183-.247.048 0 .096.008.144.024.048.016.12.048.2.08.271.12.566.215.878.279.319.064.63.096.95.096.502 0 .894-.088 1.165-.264a.86.86 0 0 0 .415-.758.777.777 0 0 0-.215-.559c-.144-.151-.416-.287-.807-.415l-1.157-.36c-.583-.183-1.014-.454-1.277-.813a1.902 1.902 0 0 1-.4-1.158c0-.335.073-.63.216-.886.144-.255.335-.479.575-.654.24-.184.51-.32.83-.415.32-.096.655-.136 1.006-.136.175 0 .359.008.535.032.183.024.35.056.518.088.16.04.312.08.455.127.144.048.256.096.336.144a.69.69 0 0 1 .24.2.43.43 0 0 1 .071.263v.375c0 .168-.064.256-.184.256a.83.83 0 0 1-.303-.096 3.652 3.652 0 0 0-1.532-.311c-.455 0-.815.071-1.062.223-.248.152-.375.383-.375.71 0 .224.08.416.24.567.159.152.454.304.877.44l1.134.358c.574.184.99.44 1.237.767.247.327.367.702.367 1.117 0 .343-.072.655-.207.926-.144.272-.336.511-.583.703-.248.2-.543.343-.886.447-.36.111-.734.167-1.142.167zM21.698 16.207c-2.626 1.94-6.442 2.969-9.722 2.969-4.598 0-8.74-1.7-11.87-4.526-.247-.223-.024-.527.272-.351 3.384 1.963 7.559 3.153 11.877 3.153 2.914 0 6.114-.607 9.06-1.852.439-.2.814.287.383.607zM22.792 14.961c-.336-.43-2.22-.207-3.074-.103-.255.032-.295-.192-.063-.36 1.5-1.053 3.967-.75 4.254-.399.287.36-.08 2.826-1.485 4.007-.215.184-.423.088-.327-.151.32-.79 1.03-2.57.695-2.994z'},
    'Mozilla': {"bbox": [1.75, 0.0, 22.249, 24.0],
        "d": 'M4.819 24H1.75V0H4.82zM7.33 12.242H19.48v-.69L11.562 8.67V6.25l7.918-2.872v-.7H10.1V0h12.149v4.89l-6.445 2.224v.69l6.445 2.224v4.89H7.33zm0-9.565h2.77v2.77H7.33z'},
    'NVIDIA': {"bbox": [0.0, 4.063, 24.0, 19.937],
        "d": 'M8.948 8.798v-1.43a6.7 6.7 0 0 1 .424-.018c3.922-.124 6.493 3.374 6.493 3.374s-2.774 3.851-5.75 3.851c-.398 0-.787-.062-1.158-.185v-4.346c1.528.185 1.837.857 2.747 2.385l2.04-1.714s-1.492-1.952-4-1.952a6.016 6.016 0 0 0-.796.035m0-4.735v2.138l.424-.027c5.45-.185 9.01 4.47 9.01 4.47s-4.08 4.964-8.33 4.964c-.37 0-.733-.035-1.095-.097v1.325c.3.035.61.062.91.062 3.957 0 6.82-2.023 9.593-4.408.459.371 2.34 1.263 2.73 1.652-2.633 2.208-8.772 3.984-12.253 3.984-.335 0-.653-.018-.971-.053v1.864H24V4.063zm0 10.326v1.131c-3.657-.654-4.673-4.46-4.673-4.46s1.758-1.944 4.673-2.262v1.237H8.94c-1.528-.186-2.73 1.245-2.73 1.245s.68 2.412 2.739 3.11M2.456 10.9s2.164-3.197 6.5-3.533V6.201C4.153 6.59 0 10.653 0 10.653s2.35 6.802 8.948 7.42v-1.237c-4.84-.6-6.492-5.936-6.492-5.936z'},
    'Netflix': {"bbox": [5.398, 0.0, 18.602, 24.0],
        "d": 'm5.398 0 8.348 23.602c2.346.059 4.856.398 4.856.398L10.113 0H5.398zm8.489 0v9.172l4.715 13.33V0h-4.715zM5.398 1.5V24c1.873-.225 2.81-.312 4.715-.398V14.83L5.398 1.5z'},
    'Cloudflare': {"bbox": [0.0, 6.573, 24.0, 17.427],
        "d": 'M16.5088 16.8447c.1475-.5068.0908-.9707-.1553-1.3154-.2246-.3164-.6045-.499-1.0615-.5205l-8.6592-.1123a.1559.1559 0 0 1-.1333-.0713c-.0283-.042-.0351-.0986-.021-.1553.0278-.084.1123-.1484.2036-.1562l8.7359-.1123c1.0351-.0489 2.1601-.8868 2.5537-1.9136l.499-1.3013c.0215-.0561.0293-.1128.0147-.168-.5625-2.5463-2.835-4.4453-5.5499-4.4453-2.5039 0-4.6284 1.6177-5.3876 3.8614-.4927-.3658-1.1187-.5625-1.794-.499-1.2026.119-2.1665 1.083-2.2861 2.2856-.0283.31-.0069.6128.0635.894C1.5683 13.171 0 14.7754 0 16.752c0 .1748.0142.3515.0352.5273.0141.083.0844.1475.1689.1475h15.9814c.0909 0 .1758-.0645.2032-.1553l.12-.4268zm2.7568-5.5634c-.0771 0-.1611 0-.2383.0112-.0566 0-.1054.0415-.127.0976l-.3378 1.1744c-.1475.5068-.0918.9707.1543 1.3164.2256.3164.6055.498 1.0625.5195l1.8437.1133c.0557 0 .1055.0263.1329.0703.0283.043.0351.1074.0214.1562-.0283.084-.1132.1485-.204.1553l-1.921.1123c-1.041.0488-2.1582.8867-2.5527 1.914l-.1406.3585c-.0283.0713.0215.1416.0986.1416h6.5977c.0771 0 .1474-.0489.169-.126.1122-.4082.1757-.837.1757-1.2803 0-2.6025-2.125-4.727-4.7344-4.727'},
    'ByteDance': {"bbox": [0.0, 1.468, 24.0, 22.531],
        "d": 'M19.8772 1.4685L24 2.5326v18.9426l-4.1228 1.0563V1.4685zm-13.3481 9.428l4.115 1.0641v8.9786l-4.115 1.0642v-11.107zM0 2.572l4.115 1.0642v16.7354L0 21.428V2.572zm17.4553 5.6205v11.107l-4.1228-1.0642V9.2568l4.1228-1.0642z'},
    'Uber': {"bbox": [0.0, 7.97, 24.0, 16.03],
        "d": 'M0 7.97v4.958c0 1.867 1.302 3.101 3 3.101.826 0 1.562-.316 2.094-.87v.736H6.27V7.97H5.082v4.888c0 1.257-.85 2.106-1.947 2.106-1.11 0-1.946-.827-1.946-2.106V7.971H0zm7.44 0v7.925h1.13v-.725c.521.532 1.257.86 2.06.86a3.006 3.006 0 0 0 3.034-3.01 3.01 3.01 0 0 0-3.033-3.024 2.86 2.86 0 0 0-2.049.861V7.971H7.439zm9.869 2.038c-1.687 0-2.965 1.37-2.965 3 0 1.72 1.334 3.01 3.066 3.01 1.053 0 1.913-.463 2.49-1.233l-.826-.611c-.43.577-.996.847-1.664.847-.973 0-1.753-.7-1.912-1.64h4.697v-.373c0-1.72-1.222-3-2.886-3zm6.295.068c-.634 0-1.098.294-1.381.758v-.713h-1.131v5.774h1.142V12.61c0-.894.544-1.47 1.291-1.47H24v-1.065h-.396zm-6.319.928c.85 0 1.564.588 1.756 1.47H15.52c.203-.882.916-1.47 1.765-1.47zm-6.732.012c1.086 0 1.98.883 1.98 2.004a1.993 1.993 0 0 1-1.98 2.001A1.989 1.989 0 0 1 8.56 13.02a1.99 1.99 0 0 1 1.992-2.004z'},
    'Valve': {"bbox": [0.0, 8.579, 24.0, 15.421],
        "d": 'M0 8.579v6.842h24V8.58zm1.8 1.415h.793l.776 3.044.76-3.044h.836l-1.227 4.029H3zm5.488 0h1.084l1.145 4.034h-.814l-.27-1.007H7.228s-.21.81-.254.99c-.242.017-.83 0-.83 0zm4.184 0h.792v3.352h1.69v.677h-2.482zm3.45 0h.816l.776 3.005.754-3.005h.815l-1.222 4.034h-.716zm4.828 0h1.69v.522h-1.084v.584h.99v.523h-.99v.6h1.084v.523h-1.69zm-11.902.68l-.426 1.702h.89z'},
    'Adobe': {"bbox": [0.0, 1.376, 24.0, 22.624],
        "d": 'M13.966 22.624l-1.69-4.281H8.122l3.892-9.144 5.662 13.425zM8.884 1.376H0v21.248zm15.116 0h-8.884L24 22.624Z'},
    'Salesforce': {"bbox": [0.0, 3.6, 24.0, 20.4],
        "d": 'M10.006 5.415a4.195 4.195 0 013.045-1.306c1.56 0 2.954.9 3.69 2.205.63-.3 1.35-.45 2.1-.45 2.85 0 5.159 2.34 5.159 5.22s-2.31 5.22-5.176 5.22c-.345 0-.69-.044-1.02-.104a3.75 3.75 0 01-3.3 1.95c-.6 0-1.155-.15-1.65-.375A4.314 4.314 0 018.88 20.4a4.302 4.302 0 01-4.05-2.82c-.27.062-.54.076-.825.076-2.204 0-4.005-1.8-4.005-4.05 0-1.5.811-2.805 2.01-3.51-.255-.57-.39-1.2-.39-1.846 0-2.58 2.1-4.65 4.65-4.65 1.53 0 2.85.705 3.72 1.8'},
    'Shopify': {"bbox": [1.448, 0.0, 22.553, 24.0],
        "d": 'M15.337 23.979l7.216-1.561s-2.604-17.613-2.625-17.73c-.018-.116-.114-.192-.211-.192s-1.929-.136-1.929-.136-1.275-1.274-1.439-1.411c-.045-.037-.075-.057-.121-.074l-.914 21.104h.023zM11.71 11.305s-.81-.424-1.774-.424c-1.447 0-1.504.906-1.504 1.141 0 1.232 3.24 1.715 3.24 4.629 0 2.295-1.44 3.76-3.406 3.76-2.354 0-3.54-1.465-3.54-1.465l.646-2.086s1.245 1.066 2.28 1.066c.675 0 .975-.545.975-.932 0-1.619-2.654-1.694-2.654-4.359-.034-2.237 1.571-4.416 4.827-4.416 1.257 0 1.875.361 1.875.361l-.945 2.715-.02.01zM11.17.83c.136 0 .271.038.405.135-.984.465-2.064 1.639-2.508 3.992-.656.213-1.293.405-1.889.578C7.697 3.75 8.951.84 11.17.84V.83zm1.235 2.949v.135c-.754.232-1.583.484-2.394.736.466-1.777 1.333-2.645 2.085-2.971.193.501.309 1.176.309 2.1zm.539-2.234c.694.074 1.141.867 1.429 1.755-.349.114-.735.231-1.158.366v-.252c0-.752-.096-1.371-.271-1.871v.002zm2.992 1.289c-.02 0-.06.021-.078.021s-.289.075-.714.21c-.423-1.233-1.176-2.37-2.508-2.37h-.115C12.135.209 11.669 0 11.265 0 8.159 0 6.675 3.877 6.21 5.846c-1.194.365-2.063.636-2.16.674-.675.213-.694.232-.772.87-.075.462-1.83 14.063-1.83 14.063L15.009 24l.927-21.166z'},
    'GitHub': {"bbox": [0.0, 0.297, 24.0, 23.703],
        "d": 'M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12'},
}

W, H = 1280, 560
TRUNK_Y = 300
R = 34            # elbow radius of a branch
TIP_GAP = 30      # distance from a logo center to its branch tip
PERIOD = 10.0     # seconds of one animation loop
TRUNK_RUN = 4.2   # seconds the trunk pulse needs to cross the banner

THEMES = {
    "dark": dict(
        bg0="#0B0F17", bg1="#0F1422", border="#1F2633", dots="#FFFFFF", dots_op=0.11,
        glow="#8957E5", glow_op=0.22, text="#F4F6FA", role="#B4BCC8", muted="#7D8796",
        label="#A98BFF", line="#2A3242", trunk_a="#2A3242", trunk_b="#A371F7",
        accent="#A371F7", pulse="#D2BCFF", logo="#DCE2EA", node_bg="#0D111B",
        num_a="#FFFFFF", num_b="#C4AAFF",
    ),
    "light": dict(
        bg0="#FFFFFF", bg1="#F6F8FA", border="#D8DEE4", dots="#1F2328", dots_op=0.10,
        glow="#8250DF", glow_op=0.10, text="#1F2328", role="#3D444D", muted="#656D76",
        label="#8250DF", line="#D6DCE3", trunk_a="#D6DCE3", trunk_b="#8250DF",
        accent="#8250DF", pulse="#8250DF", logo="#1F2328", node_bg="#FFFFFF",
        num_a="#1F2328", num_b="#6639BA",
    ),
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

TITLE = (
    "Alexandre Kohler, Senior Full Stack Software Engineer, backend, APIs and microservices, "
    "open source contributor to Google, Microsoft, Meta, Apple and Amazon"
)
DESC = (
    "Alexandre Kohler (kwy404), Senior Full Stack Software Engineer in Brusque, SC, Brazil (UTC-3), "
    "with more than 10 years of full stack experience in backend systems, APIs and microservices "
    "using TypeScript, Node.js, NestJS, Python, Go, Rust, PHP, Java, React and AWS. "
    f"{MERGED_PRS} merged pull requests in {ORGS} organizations, including Google, Microsoft, Meta, Apple, "
    "Amazon Web Services, Mozilla, NVIDIA, Netflix, Cloudflare, ByteDance, Uber, Valve, Adobe, Salesforce, "
    "Shopify and GitHub, drawn as branches that leave one main line."
)


def logo_size(name):
    x0, y0, x1, y1 = LOGOS[name]["bbox"]
    w, h = x1 - x0, y1 - y0
    area = 28.5 ** 2
    if w / h > 2:
        area *= 1.35
    s = min(math.sqrt(area / (w * h)), 31 / h, 58 / w)
    return w * s, h * s


def logo_uri(name, color):
    x0, y0, x1, y1 = LOGOS[name]["bbox"]
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:g} {y0:g} {x1 - x0:g} {y1 - y0:g}">'
        f'<path fill="{color}" d="{LOGOS[name]["d"]}"/></svg>'
    )
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("ascii")


def row_layout(names, x0, x1):
    sizes = [logo_size(n) for n in names]
    total = sum(w for w, _ in sizes)
    gap = (x1 - x0 - total) / (len(names) - 1)
    x, out = x0, []
    for n, (w, h) in zip(names, sizes):
        out.append((n, x + w / 2, w, h))
        x += w + gap
    return out


def build(theme, logo_y_top=172, logo_y_bot=428):
    t = THEMES[theme]
    top = row_layout(TOP, 664, 1180)
    bot = row_layout(BOTTOM, 700, 1220)
    trunk_x0, trunk_x1 = 24, 1256
    trunk_len = trunk_x1 - trunk_x0
    pulse_len = 110

    css = [
        f".tp{{stroke-dasharray:{pulse_len} {trunk_len + pulse_len + 40};stroke-dashoffset:{pulse_len};"
        f"animation:tp {PERIOD}s linear infinite}}",
        f"@keyframes tp{{0%{{stroke-dashoffset:{pulse_len}}}"
        f"{TRUNK_RUN / PERIOD * 100:.2f}%,100%{{stroke-dashoffset:{-trunk_len}}}}}",
        ".bp{stroke-dashoffset:var(--o);animation:bp " + f"{PERIOD}s" + " cubic-bezier(.3,0,.2,1) infinite}",
        "@keyframes bp{0%{stroke-dashoffset:var(--o)}9%,100%{stroke-dashoffset:var(--e)}}",
        ".pg{opacity:0;transform-box:fill-box;transform-origin:center;animation:pg " + f"{PERIOD}s" + " ease-out infinite}",
        "@keyframes pg{0%{opacity:.9;transform:scale(1)}10%,100%{opacity:0;transform:scale(3.4)}}",
        "@media (prefers-reduced-motion:reduce){.tp,.bp,.pg{animation:none}}",
    ]

    branches, pulses, pings, tips, images = [], [], [], [], []
    bp_dash = 30
    for row, ly, sign in ((top, logo_y_top, -1), (bot, logo_y_bot, 1)):
        for name, xc, w, h in row:
            xs = xc - R
            tip_y = ly - sign * TIP_GAP
            k = 0.5523 * R
            ey = TRUNK_Y + sign * R
            d = (
                f"M{xs:.1f} {TRUNK_Y}C{xs + k:.1f} {TRUNK_Y} {xc:.1f} {TRUNK_Y + sign * (R - k):.1f} "
                f"{xc:.1f} {ey:.1f}L{xc:.1f} {tip_y:.1f}"
            )
            length = math.pi * R / 2 + abs(tip_y - ey)
            branches.append(d)
            # when the trunk pulse front reaches xs
            start = TRUNK_RUN * (xs - trunk_x0) / (trunk_len + pulse_len)
            pulses.append(
                f'<path class="bp" d="{d}" stroke-dasharray="{bp_dash} {length + bp_dash + 20:.0f}" '
                f'style="--o:{bp_dash};--e:{-length:.0f};animation-delay:{start:.2f}s"/>'
            )
            arrive = start + 0.56
            pings.append(
                f'<circle class="pg" cx="{xc:.1f}" cy="{tip_y:.1f}" r="4" style="animation-delay:{arrive:.2f}s"/>'
            )
            tips.append(f'<circle cx="{xc:.1f}" cy="{tip_y:.1f}" r="3.6"/>')
            images.append(
                f'<image x="{xc - w / 2:.1f}" y="{ly - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
                f'href="{logo_uri(name, t["logo"])}"><title>{name}</title></image>'
            )

    # commit dots on the left part of the trunk, the history before the branches
    history = [64, 160, 256, 352, 448, 544]
    hist = "".join(
        f'<circle cx="{x}" cy="{TRUNK_Y}" r="{4.4 if j == 0 else 3.2}"/>' for j, x in enumerate(history)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">{TITLE}</title>
<desc id="d">{DESC}</desc>
<style>{"".join(css)}</style>
<defs>
<clipPath id="card"><rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16"/></clipPath>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["bg0"]}"/><stop offset="1" stop-color="{t["bg1"]}"/></linearGradient>
<radialGradient id="glow" cx="930" cy="{TRUNK_Y}" r="520" gradientUnits="userSpaceOnUse" gradientTransform="translate(930 {TRUNK_Y}) scale(1 .62) translate(-930 -{TRUNK_Y})"><stop offset="0" stop-color="{t["glow"]}" stop-opacity="{t["glow_op"]}"/><stop offset="1" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.1" fill="{t["dots"]}"/></pattern>
<radialGradient id="fade" cx="940" cy="{TRUNK_Y}" r="560" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset=".55" stop-color="#fff" stop-opacity=".5"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="gridmask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<linearGradient id="trunk" gradientUnits="userSpaceOnUse" x1="{trunk_x0}" y1="0" x2="{trunk_x1}" y2="0"><stop offset="0" stop-color="{t["trunk_a"]}" stop-opacity="0"/><stop offset=".08" stop-color="{t["trunk_a"]}"/><stop offset=".46" stop-color="{t["trunk_a"]}"/><stop offset=".78" stop-color="{t["trunk_b"]}"/><stop offset=".97" stop-color="{t["trunk_b"]}" stop-opacity=".9"/><stop offset="1" stop-color="{t["trunk_b"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="pulse" gradientUnits="userSpaceOnUse" x1="{trunk_x0}" y1="0" x2="{trunk_x1}" y2="0"><stop offset="0" stop-color="{t["pulse"]}" stop-opacity="0"/><stop offset=".1" stop-color="{t["pulse"]}"/><stop offset=".95" stop-color="{t["pulse"]}"/><stop offset="1" stop-color="{t["pulse"]}" stop-opacity="0"/></linearGradient>
<linearGradient id="num" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["num_a"]}"/><stop offset="1" stop-color="{t["num_b"]}"/></linearGradient>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridmask)" opacity="{t["dots_op"]}"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{t["border"]}"/>

<g font-family="{SANS}">
<text x="64" y="84" font-family="{MONO}" font-size="13.5" letter-spacing="2.2" fill="{t["label"]}">KWY404  ·  BRUSQUE, SC, BRAZIL  ·  UTC-3</text>
<text x="61" y="160" font-size="68" font-weight="700" letter-spacing="-2.2" fill="{t["text"]}">Alexandre Kohler</text>
<text x="64" y="205" font-size="28" font-weight="500" letter-spacing="-.3" fill="{t["role"]}">Senior Full Stack Software Engineer</text>
<text x="64" y="244" font-size="17" fill="{t["muted"]}">10+ years building backend systems, APIs and microservices</text>
</g>

<path d="M{trunk_x0} {TRUNK_Y}H{trunk_x1}" stroke="url(#trunk)" stroke-width="2.2" fill="none"/>
<g fill="none" stroke="{t["line"]}" stroke-width="1.6" stroke-linecap="round">{"".join(f'<path d="{d}"/>' for d in branches)}</g>
<g fill="{t["node_bg"]}" stroke="{t["trunk_a"]}" stroke-width="2">{hist}</g>
<g filter="url(#soft)" fill="none" stroke-linecap="round">
<path class="tp" d="M{trunk_x0} {TRUNK_Y}H{trunk_x1}" stroke="url(#pulse)" stroke-width="2.6"/>
<g stroke="{t["pulse"]}" stroke-width="2.2">{"".join(pulses)}</g>
</g>
<g fill="none" stroke="{t["accent"]}" stroke-width="1.5">{"".join(pings)}</g>
<g fill="{t["accent"]}" stroke="{t["node_bg"]}" stroke-width="3" paint-order="stroke">{"".join(tips)}</g>
<g>{"".join(images)}</g>

<g font-family="{SANS}">
<text x="62" y="430" font-size="76" font-weight="700" letter-spacing="-3" fill="url(#num)">{MERGED_PRS}</text>
<text x="64" y="462" font-size="15.5" fill="{t["muted"]}">merged pull requests</text>
<text x="272" y="430" font-size="76" font-weight="700" letter-spacing="-3" fill="url(#num)">{ORGS}</text>
<text x="274" y="462" font-size="15.5" fill="{t["muted"]}">organizations</text>
<text x="64" y="516" font-family="{MONO}" font-size="13" letter-spacing=".4" fill="{t["muted"]}">TypeScript · Node.js · Python · Go · Rust · PHP · React · AWS</text>
</g>
<text x="64" y="284" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{t["muted"]}">main</text>
<text x="1216" y="84" text-anchor="end" font-family="{MONO}" font-size="13.5" letter-spacing="2.2" fill="{t["muted"]}">MERGED UPSTREAM AT</text>
</svg>
'''
    return svg


if __name__ == "__main__":
    for theme in THEMES:
        svg = build(theme)
        (HERE / f"{theme}.svg").write_text(svg, encoding="utf-8", newline=chr(10))
        print(f"{theme}.svg", len(svg.encode("utf-8")), "bytes")
