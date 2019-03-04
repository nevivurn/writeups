package io.michaelrocks.paranoid;

import android.support.v4.internal.view.SupportMenu;

public class Deobfuscator$app$Debug {
    private static final String[] charChunks = new String[]{"}18m_hanbed3i{0g"};
    private static final String[] indexChunks = new String[]{"\u000f\f\u000f\t\u0003\r\u0005\f\n\n\t\u0007\u0004\u0002\u0001\u0006\t\b\u000e\u0001\u000b\b\t\u0006\u0000"};
    private static final String[] locationChunks = new String[]{"\u0000\u0000\u0019\u0000"};

    public static String getString(int id) {
        int location1Index = id % 4096;
        int location2ChunkIndex = (id + 1) / 4096;
        int location2Index = (id + 1) % 4096;
        String locations1 = locationChunks[id / 4096];
        String locations2 = locationChunks[location2ChunkIndex];
        int offset1 = ((locations1.charAt((location1Index * 2) + 1) & SupportMenu.USER_MASK) << 16) | (locations1.charAt(location1Index * 2) & SupportMenu.USER_MASK);
        int length = ((locations2.charAt((location2Index * 2) + 1) << 16) | locations2.charAt(location2Index * 2)) - offset1;
        char[] stringChars = new char[length];
        for (int i = 0; i < length; i++) {
            int offset = offset1 + i;
            int indexIndex = offset % 8192;
            int index = indexChunks[offset / 8192].charAt(indexIndex) & SupportMenu.USER_MASK;
            int charIndex = index % 8192;
            stringChars[i] = charChunks[index / 8192].charAt(charIndex);
        }
        return new String(stringChars);
    }
}
