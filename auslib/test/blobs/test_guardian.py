import pytest

from auslib.blobs.guardian import GuardianBlob


@pytest.fixture(scope="session")
def guardianblob():
    blob = GuardianBlob()
    blob.loadJSON(
        """
{
    "name": "Guardian-1.0.0.0",
    "product": "Guardian",
    "schema_version": 10000,
    "version": "1.0.0.0",
    "required": true,
    "platforms": {
        "WINNT_x86_64": {
            "fileUrl": "https://a.com/this/is/1.0.0.0.msi"
        },
        "Darwin_x86_64": {
            "fileUrl": "https://a.com/this/is/1.0.0.0.dmg"
        }
    }
}
"""
    )
    return blob


@pytest.mark.parametrize("whitelistedDomains,expected", [({"a.com": ("Guardian",)}, False), ({}, True)])
def testContainsForbiddenDomain(guardianblob, whitelistedDomains, expected):
    assert guardianblob.containsForbiddenDomain("Guardian", whitelistedDomains) is expected


@pytest.mark.parametrize(
    "version,expected", [("0.5.0.0", True), ("0.8.0.0", True), ("0.99.99.99", True), ("1.0.0.0", False), ("1.0.5.0", False), ("2.0.0.0", False)]
)
def testShouldServeUpdateVariousVersions(guardianblob, version, expected):
    updateQuery = {"product": "Guardian", "version": version, "buildTarget": "WINNT_x86_64", "channel": "release"}
    assert guardianblob.shouldServeUpdate(updateQuery) is expected


def testShouldServeUpdateMissingBuildTarget(guardianblob):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": "Linux_x86_64", "channel": "release"}
    assert not guardianblob.shouldServeUpdate(updateQuery)


@pytest.mark.parametrize(
    "buildTarget,whitelistedDomains,expected",
    [
        ("WINNT_x86_64", {"a.com": ("Guardian",)}, {"required": True, "url": "https://a.com/this/is/1.0.0.0.msi", "version": "1.0.0.0"}),
        ("Darwin_x86_64", {"a.com": ("Guardian",)}, {"required": True, "url": "https://a.com/this/is/1.0.0.0.dmg", "version": "1.0.0.0"}),
        ("Linux_x86_64", {"a.com": ("Guardian",)}, {}),
        ("WINNT_x86_64", {}, {}),
    ],
)
def testGetResponse(guardianblob, buildTarget, whitelistedDomains, expected):
    updateQuery = {"product": "Guardian", "version": "0.5.0.0", "buildTarget": buildTarget, "channel": "release"}
    assert guardianblob.getResponse(updateQuery, whitelistedDomains) == expected
